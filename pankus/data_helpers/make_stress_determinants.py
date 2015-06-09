#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.line_conn import line_conn
from pankus.storages.turn_info import turn_info
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import *


def make_stress_determinants():

    line_conn.update_many({}, {"$unset":
                               {"intl_determinant": "",
                                "junc_determinant": ""}})
    pbar = Pbar('junction stress: ',line_conn.count())

    for stress_line in line_conn.find():
        pbar.plus_one()
        start = stress_line[start_key]
        end = stress_line[end_key]
        # stress doesnt have to be ordered
        # print stress_line
        ordered_intl = stress_line['ordered_intl']
        # print stress_line
        ordered_junc = stress_line['ordered_junc']

        line_conn.update_one({start_key: start, end_key: end},
                             {"$set":
                              {"intl_determinant": sum(
                                  map(sum, ordered_intl)) -
                                  ordered_intl[0][0] - ordered_intl[-1][-1]}
                              })
        line_conn.update_many({end_key: end},
                              {"$inc":
                               {"junc_determinant": sum(
                                   ordered_junc) - ordered_junc[0]}
                               })
    pbar.finish()

if __name__ == "__main__":
    make_stress_determinants()
