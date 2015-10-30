#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.helpers.pbar import Pbar
from pankus.storages.line_conn import line_conn
from pankus.data_helpers.make_junction_turn_info import make_junction_turn_info
from pankus.storages.turn_info import turn_info
from pankus.storages.stress import stress


def save_stress_to_line_conn():

    if turn_info.count() == 0:
        make_junction_turn_info()


    pbar = Pbar('saving : ',line_conn.count())

    lc=[]
    for edge in line_conn.find():

        assert len(list(line_conn.find({
            start_key: edge[start_key],
            end_key: edge[end_key]
        }))) == 1
        assert ordered_junction_info_key not in edge
        assert stress_key not in edge
        assert ordered_interlace_info_key not in edge

        pbar.plus_one()
        start = edge[start_key]
        end = edge[end_key]

        # ordered list from turn info
        ordered_successors_list = turn_info.find_one(
            {start_key: start, end_key: end})[ordered_successors_key]

        ordered_predecessors_list = turn_info.find_one(
            {start_key: start, end_key: end})[ordered_predecessors_key]

        # create empty dicts for gathered info
        edge_stress = 0
        junction_stress = dict([
                                (i, 0) for i in ordered_successors_list
                                ])

        interlace_stress = dict([
                                    (i, dict([
                                                (j, 0) for j in ordered_successors_list
                                            ])
                                     ) for i in ordered_predecessors_list
                                ])

        # each stress append to its proper place
        for stress_element in stress.find({start_key: start, end_key: end}):
            edge_stress += stress_element.get(stress_key,0)

            for out_id in stress_element.get(junction_key,[]):
                junction_stress[int(out_id)] += stress_element[junction_key][out_id]

            for in_id in stress_element.get(interlace_key,[]):
                for out_id in stress_element[interlace_key][in_id]:
                    interlace_stress[int(in_id)][int(out_id)] +=\
                        stress_element[interlace_key][in_id][out_id]

        # make order in gathered data
        ordered_junc = [junction_stress[i] for i in ordered_successors_list]

        ordered_intl = [[interlace_stress[j][i]
                         for i in ordered_successors_list
                            ] for j in ordered_predecessors_list
                        ]

        edge[stress_key]=edge_stress
        edge[ordered_junction_info_key]=ordered_junc
        edge[ordered_interlace_info_key]=ordered_intl
        lc.append(edge)
    line_conn.delete_many({})
    line_conn.insert_many(lc)

    pbar.finish()


if __name__ == "__main__":
    save_stress_to_line_conn()