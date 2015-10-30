#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.line_conn import line_conn
from pankus.storages.turn_info import turn_info
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection

def make_stress_determinants():

    pbar = Pbar('junction stress: ',2*line_conn.count())
    ram_line_conn=RamCollection(line_conn)

    for line in ram_line_conn.find():
        pbar.plus_one()
        assert ordered_interlace_info_key in line
        assert ordered_junction_info_key in line

        line[junction_determinant_key]=0
        line[interlace_determinant_key]=0

    for line in ram_line_conn.find():
        pbar.plus_one()
        start = line[start_key]
        end = line[end_key]
        # stress doesnt have to be ordered
        # print stress_line
        ordered_intl = line[ordered_interlace_info_key]
        # print stress_line
        ordered_junc = line[ordered_junction_info_key]

        lc=ram_line_conn.find_one({
            start_key:start,
            end_key:end
        })
        lc[interlace_determinant_key]=sum(map(sum, ordered_intl)) -\
                                  ordered_intl[0][0] - ordered_intl[-1][-1]
        lc[junction_determinant_key] += sum(ordered_junc) -\
                                        ordered_junc[0]
    line_conn.delete_many({})
    line_conn.insert_many(ram_line_conn.find())

    pbar.finish()

if __name__ == "__main__":
    make_stress_determinants()
