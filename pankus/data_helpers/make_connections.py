#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.line_conn import line_conn
from pankus.storages.stress import stress
from pankus.storages.connection import connection
from pankus.stress.weight_increase_function import weight_increase_function
from pankus.helpers.pbar import Pbar

def make_connections():
    new_conn = []
    pbar = Pbar('make conn: ', line_conn.count())
    for edge in line_conn.find():
        pbar.plus_one()
        assert weight_key in edge

        stress_amount = sum([stress_part.get(stress_key, 0)
                             for stress_part in stress.find({
                start_key: edge[start_key],
                end_key: edge[end_key]
            })
                             ])

        throughput = line_conn.find_one({
            start_key: edge[start_key], end_key: edge[end_key]})[throughput_key]

        if throughput > 0 and stress_amount > 0 and edge[weight_key] < sd_surplus:
            new_conn.append({
                start_key: edge[start_key],
                end_key: edge[end_key],
                weight_key: edge[weight_key] *
                            weight_increase_function(stress_amount / throughput)
            })
        else:
            new_conn.append({
                start_key: edge[start_key],
                end_key: edge[end_key],
                weight_key: edge[weight_key]
            })
    connection.delete_many({})
    connection.insert_many(new_conn)
    pbar.finish()


if __name__ == "__main__":
    make_connections()
