#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import cmath
from pankus.helpers.pbar import Pbar
from pankus.storages.line_conn import line_conn as line_conn
from pankus.storages.turn_info import turn_info


def make_junction_turn_info():
    pbar = Pbar('junction info: ',line_conn.count())
    turn_info.delete_many({})
    new_turn_info = []
    for raw_line in line_conn.find():
        assert len(list(line_conn.find({
            start_key: raw_line[start_key],
            end_key: raw_line[end_key]
        }))) == 1

        pbar.plus_one()
        start_id = raw_line[start_key]
        end_id = raw_line[end_key]
        start_vector = complex(*raw_line[linestring_key][1]) - complex(
            *raw_line[linestring_key][0])
        end_vector = complex(*raw_line[linestring_key][-1]) - complex(
            *raw_line[linestring_key][-2])

        predecessors_angles = {}

        for prv_line in line_conn.find({end_key: start_id}):
            end_predecessors_vector = \
                complex(*prv_line[linestring_key][-1]) - \
                complex(*prv_line[linestring_key][-2])
            angle = cmath.phase(start_vector / end_predecessors_vector)
            predecessors_angles[angle] = prv_line[start_key]
        predecessors_ordered_list = [predecessors_angles[a]
                                     for a in sorted(predecessors_angles)]

        successors_angles = {}

        for succ_line in line_conn.find({start_key: end_id}):
            start_successors_vector = \
                complex(*succ_line[linestring_key][1]) - \
                complex(*succ_line[linestring_key][0])
            angle = cmath.phase(start_successors_vector / end_vector)
            successors_angles[angle] = succ_line[end_key]
        successors_ordered_list = [successors_angles[a]
                                   for a in sorted(successors_angles)]

        new_turn_info.append(
            {start_key: start_id,
             end_key: end_id,
             ordered_predecessors_key: predecessors_ordered_list,
             ordered_successors_key: successors_ordered_list
             })
    turn_info.insert_many(new_turn_info)
    pbar.finish()


if __name__ == "__main__":
    make_junction_turn_info()
