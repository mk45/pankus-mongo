#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from heapq import heappush as pqpush
from heapq import heappop as pqpop
from pankus.helpers.pbar import Pbar
from pankus.helpers.start_cached_collection import StartCachedCollection
from pankus.storages.dendryt import dendryt
from pankus.storages.featured_point import featured_point
from pankus.storages.connection import connection
from pankus.storages.path import path
from pankus.defaults.config import \
    start_key,end_key,sd_surplus,id_key,weight_key,path_key,\
    predecessor_key,delta_key,successor_key
import argparse,ipdb


def make_kpaths(k_paths):
    path.delete_many({})
    pbar = Pbar('k paths: ',featured_point.count())
    ram_dendryt=StartCachedCollection(dendryt,start_key,end_key)
    for sd_start in featured_point.find():
        start = sd_start[id_key]
        pbar.plus_one()

        for sd_end in featured_point.find():
            end = sd_end[id_key]
            # print sd_start, sd_end

            if start == end:
                continue
            if k_paths > 1:
                P = []
                H = []  # list pq
                pqpush(H, (0, [end]))

                for k in xrange(k_paths):

                    if H != []:
                        minkrt = pqpop(H)
                    else:
                        # No more avilible paths
                        break

                    while minkrt[1][0] != start:
                        # print minkrt
                        #####################################################
                        # watch here for search speedup/cut
                        # dont search paths twice as long as shortes one (2)
                        # search paths with weights at least up to 100
                        if P != [] and minkrt[0] / 2 > ram_dendryt.find_one(
                                {start_key: start, end_key: end})[weight_key] -\
                                2 * sd_surplus + 100:
                            break
                        minkrt_list = minkrt[1]
                        for edge in connection.find({end_key: minkrt_list[0]}):

                            edge_weight = edge[weight_key]
                            edge_start_id = edge[start_key]

                            if edge_start_id not in minkrt_list:
                                inserted = (
                                    minkrt[0] -
                                    ram_dendryt.find_one(
                                        {start_key: start,
                                         end_key: minkrt_list[0]})[weight_key] +
                                    ram_dendryt.find_one(
                                        {start_key: start,
                                         end_key: edge_start_id})[weight_key] +
                                    edge_weight,
                                    list([edge_start_id] + minkrt_list)
                                )
                                pqpush(H, inserted)
                        minkrt = pqpop(H)

                    else:
                        # if while loop ends up normally
                        P.append({start_key: start, end_key: end,
                                  path_key: minkrt[1],
                                  delta_key: minkrt[0],
                                  weight_key: minkrt[0] + \
                                              ram_dendryt.find_one({
                                                  start_key: start,
                                                  end_key: end
                                              })[weight_key]
                                  })

                        # continue for loop
                        continue
                    break
                    # if reaks up abnormally by brake ; than brake outer for

                assert len(P) > 0
                path.insert_many(P)
            else:
                Pth = []
                current_node = end
                while current_node != start:
                    Pth.append(current_node)
                    next_node = ram_dendryt.find_one(
                        {start_key: start,
                         end_key: current_node})

                    assert next_node[predecessor_key]==start or \
                        next_node[predecessor_key] != current_node

                    current_node=next_node[predecessor_key]
                Pth.append(current_node)
                Pth.reverse()
                path.insert_one({start_key: start,
                                 end_key: end,
                                 path_key: Pth,
                                 delta_key: 0,
                                 weight_key: ram_dendryt.find_one({
                                     start_key: start,
                                     end_key: end
                                 })[weight_key]
                                 })

    pbar.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", default=1, nargs='?', type=int)
    args = parser.parse_args()

    make_kpaths(args.paths)
