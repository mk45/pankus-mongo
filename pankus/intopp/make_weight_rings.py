#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.ring import ring
from pankus.storages.featured_point import featured_point
from pankus.storages.dendryt import dendryt
from pankus.helpers.start_cached_collection import StartCachedCollection
from pankus.helpers.ram_collection import RamCollection
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    start_key,end_key,id_key,weight_key,\
    sd_start_key,sd_end_key,sd_id_key,\
    ring_key,sd_surplus
import argparse


# weight delta in weight units
def make_weight_rings(weight_delta,center_in_ring_zero=False):
    """
    Makes rings
    :param weight_delta: Delta between rings. if weight in seconds this is also in seconds
    :center_in_ring_zero: Only center in ring zero
    """

    assert weight_delta > 0
    ring.delete_many({})
    new_ring=[]
    pbar = Pbar('make rings : ',featured_point.count())

    ram_dendryt = StartCachedCollection(dendryt,start_key,end_key)
    #ram_dendryt=RamCollection(dendryt,[start_key,end_key])
    for start_point in featured_point.find():
        pbar.plus_one()
        for end_point in featured_point.find():
            weight = ram_dendryt.find_one(
                {start_key: start_point[id_key],
                 end_key: end_point[id_key]})[weight_key]

            if weight >0:
                ring_number = int((weight-2*sd_surplus) / weight_delta)
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
    make_weight_rings(args.delta)
