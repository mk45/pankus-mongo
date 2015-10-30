#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import argparse
from pankus.storages.motion_exchange import motion_exchange
from pankus.storages.stress_matrix import stress_matrix
from pankus.storages.featured_point \
    import featured_point as featured_point
from pankus.helpers.pbar import Pbar


def make_stress_matrix(fraction):

    new_sm = []
    pbar = Pbar('stress matrix: ',motion_exchange.count())
    for record in motion_exchange.find():
        pbar.plus_one()
        start_id = featured_point.find_one({sd_id_key: record[sd_start_key]})[id_key]
        end_id = featured_point.find_one({sd_id_key: record[sd_end_key]})[id_key]
        quantity = float(record[motion_quantity_key]) * fraction
        new_sm.append({start_key: start_id, end_key: end_id, motion_quantity_key: quantity})
    stress_matrix.delete_many({})
    stress_matrix.insert_many(new_sm)
    pbar.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fraction", default=0.01, nargs='?', type=float)
    args = parser.parse_args()

    make_stress_matrix(args.divide)
