#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from math import sqrt
from pankus.storages.ring import ring
from pankus.storages.featured_point import featured_point
from pankus.storages.dendryt import dendryt
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    start_key,end_key,id_key,weight_key,\
    sd_start_key,sd_end_key,sd_id_key,\
    ring_key,sd_surplus

import argparse


# weight delta in weight units
def make_sqr_increase_rings(first_ring_weight_delta,center_in_ring_zero=False):
    """
    Makes rings
    :param first_ring_weight_delta: Delta of first ring in weight units if weight in seconds this is also in seconds
    :center_in_ring_zero: Only center in ring zero
    """

    assert first_ring_weight_delta > 0
    ring.delete_many({})
    new_ring=[]
    pbar = Pbar('make rings : ',featured_point.count())
    for start_point in featured_point.find():
        pbar.plus_one()
        for end_point in featured_point.find():
            weight = dendryt.find_one(
                {start_key: start_point[id_key],
                 end_key: end_point[id_key]})[weight_key]

            if weight >0:
                ring_number = int(sqrt((weight-2*sd_surplus)/first_ring_weight_delta))
                if center_in_ring_zero:
                    ring_number+=1
            else:
                ring_number = 0

            new_ring.append({
                sd_start_key: start_point[sd_id_key],
                sd_end_key: end_point[sd_id_key],
                ring_key: ring_number
            })
    ring.insert_many(new_ring)
    pbar.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("delta", type=float)
    args = parser.parse_args()
    make_sqr_increase_rings(args.delta)
