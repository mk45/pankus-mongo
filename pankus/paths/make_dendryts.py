#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from heapq import heappush as pqpush
from heapq import heappop as pqpop
from pankus.storages.dendryt import dendryt
from pankus.storages.featured_point import featured_point
from pankus.storages.point import point
from pankus.storages.connection import connection
from pankus.defaults.config import \
    sd_surplus, id_key, start_key, end_key, weight_key, successor_key, predecessor_key
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection


def make_dendryts():
    """
    
    Makes all dendryts for featured points
    """

    # this line gives you speed
    conn = RamCollection(connection)
    # conn=connection

    dendryt.delete_many({})
    N = point.count()
    pbar = Pbar('all dendryts: ', featured_point.count())

    sd_id_list = [sd_id[id_key] for sd_id in featured_point.find()]

    for start in sd_id_list:
        pbar.plus_one()

        H = []
        new_dendryt = [{
                           start_key: start,
                           end_key: i,
                           weight_key: float('inf'),
                           successor_key: None,
                           predecessor_key: None
                       } for i in xrange(N)]
        Used = [False for i in xrange(N)]
        new_dendryt[start][weight_key] = 0
        new_dendryt[start][predecessor_key] = start
        new_dendryt[start][successor_key] = start
        Used[start] = True
        for edge in conn.find({start_key: start}):
            end = edge[end_key]
            weight = edge[weight_key]
            new_dendryt[end] = {
                start_key: start,
                end_key: end,
                weight_key: weight,
                successor_key: end,
                predecessor_key: start
            }
            pqpush(H, (weight, end))

        while H != []:
            n_id = pqpop(H)[1]
            if Used[n_id]:
                continue
            Used[n_id] = True
            for edge in conn.find({start_key: n_id}):
                end_id = edge[end_key]
                weight = edge[weight_key]
                if new_dendryt[end_id][weight_key] > new_dendryt[n_id][weight_key] + weight:
                    new_dendryt[end_id][weight_key] = new_dendryt[n_id][weight_key] + weight
                    new_dendryt[end_id][successor_key] = new_dendryt[n_id][successor_key]
                    new_dendryt[end_id][predecessor_key] = n_id
                    pqpush(H, (new_dendryt[end_id][weight_key], end_id))

        dendryt.insert_many(new_dendryt)

        if sd_surplus > 0:
            # no infinity distances allowed no excide 'max lenghts' or sd_surplus
            assert all(
                [d[weight_key] < 3 * sd_surplus
                 for d in new_dendryt if d[end_key] in sd_id_list])
        else:
            assert all(
                [d[weight_key] < float('inf')
                 for d in new_dendryt if d[end_key] in sd_id_list])

    pbar.finish()


if __name__ == "__main__":
    make_dendryts()
