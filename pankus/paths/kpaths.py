#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storage.start_cached_dendryt import start_cached_dendryt as dendryt
from pankus.storage.featured_point import featured_point
from pankus.storage.ram_conn import ram_conn as conn
from pankus.storage.path import path
from pankus.defaults.sd_surplus import sd_surplus
from heapq import heappush as pqpush
from heapq import heappop as pqpop
from pankus.helpers.pbar import Pbar
import argparse
# import ipdb


def kpaths(k_paths):
    path.drop()
    pbar = Pbar('k paths: ',featured_point.count())

    for sd_start in featured_point.find():
        start = sd_start['id']
        pbar.plus_one()

        for sd_end in featured_point.find():
            end = sd_end['id']
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
                        if P != [] and minkrt[0] / 2 > dendryt.find_one(
                                {start_key: start, end_key: end})['w'] -\
                                2 * sd_surplus + 100:
                            break
                        minkrt_list = minkrt[1]
                        for edge in conn.find({end_key: minkrt_list[0]}):

                            edge_weight = edge['w']
                            edge_start_id = edge[start_key]

                            if edge_start_id not in minkrt_list:
                                inserted = (
                                    minkrt[0] -
                                    dendryt.find_one(
                                        {start_key: start,
                                         end_key: minkrt_list[0]})['w'] +
                                    dendryt.find_one(
                                        {start_key: start,
                                         end_key: edge_start_id})['w'] +
                                    edge_weight,
                                    list([edge_start_id] + minkrt_list)
                                )
                                pqpush(H, inserted)
                        minkrt = pqpop(H)

                    else:
                        # if while loop ends up normally
                        P.append({start_key: start, end_key: end,
                                  'path': minkrt[1],
                                  'd': minkrt[0],
                                  'w': minkrt[0] + dendryt.find_one(
                                      {start_key: start, end_key: end})['w']})

                        # continue for loop
                        continue
                    break
                    # if reaks up abnormally by brake ; than brake outer for

                assert len(P) > 0
                path.insert_many(P)
            else:
                Pth = []
                currentnode = end
                while currentnode != start:
                    Pth.append(currentnode)
                    currentnode = dendryt.find_one(
                        {start_key: start,
                         end_key: currentnode})['y']
                Pth.append(currentnode)
                Pth.reverse()
                path.insert_one({start_key: start, end_key: end,
                                 'path': Pth, 'd': 0,
                                 'w': dendryt.find_one(
                                     {start_key: start, end_key: end})['w']})

    pbar.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", default=1, nargs='?', type=int)
    args = parser.parse_args()

    kpaths(args.paths)
