#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.sd_point import sd_point
from pankus.storages.src_dst import src_dst
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    sd_id_key,sources_key,destinations_key,selectivity_key
import argparse


def make_src_dst(selectivity=None):
    """

    :param selectivity: selectivity in part per million
    makes selectivity or takes it from input data
    """
    new_src_dst = []
    pbar = Pbar('make src_dst: ',sd_point.count())
    for point in sd_point.find():
        pbar.plus_one()
        if selectivity:
            new_src_dst.append({
                sd_id_key: point[sd_id_key],
                sources_key: point[sources_key],
                destinations_key: point[destinations_key],
                selectivity_key: selectivity

            })
        else:
            assert selectivity_key in point
            new_src_dst.append({
                sd_id_key: point[sd_id_key],
                sources_key: point[sources_key],
                destinations_key: point[destinations_key],
                selectivity_key: point[selectivity_key]
            })
    src_dst.delete_many({})
    src_dst.insert_many(new_src_dst)
    pbar.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "selectivity",
        help="in parts per million",
        default=10, nargs='?', type=float)
    args = parser.parse_args()
    make_src_dst(args.selectivity)
