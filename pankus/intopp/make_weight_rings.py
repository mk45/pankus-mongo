#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.ring import ring
from pankus.storages.featured_point import featured_point
from pankus.storages.dendryt import dendryt
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    start_key,end_key,id_key,weight_key,\
    sd_start_key,sd_end_key,sd_id_key,ring_key
import argparse


# weight delta in weight units
def make_weight_rings(weight_delta):
    """
    Makes rings
    :param weight_delta: Delta between rings. if weight in seconds this is also in seconds

    """

    assert weight_delta > 0
    ring.delete_many({})
    new_ring=[]
    pbar = Pbar('make rings : ',featured_point.count())
    for start_point in featured_point.find():
        pbar.plus_one()
        for end_point in featured_point.find():
            weight = dendryt.find_one(
                {start_key: start_point[id_key],
                 end_key: end_point[id_key]})[weight_key]
            ring_number = int(weight / weight_delta)
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
    make_weight_rings(args.delta)
