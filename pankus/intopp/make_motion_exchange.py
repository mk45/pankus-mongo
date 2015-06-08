#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.ring import ring
from pankus.storages.ring_total import ring_total
from pankus.storages.src_dst import src_dst
from pankus.storages.motion_exchange import motion_exchange
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    sd_id_key,sd_start_key,sd_end_key,ring_key,to_ring_total_key,\
    in_ring_total_key,selectivity_key,sources_key,destinations_key,motion_quantity_key
import math


def make_motion_exchange():
    """
    Makes motion exchange for intervening opportunities model
    simple one pre-step of intervening opportunities iteration
    simple but with idea core
    """
    pbar = Pbar('make motion exchange: ',src_dst.count())
    motion_exchange.delete_many({})
    for src_point in src_dst.find():
        pbar.plus_one()
        me = []
        for dst_point in src_dst.find():
            r = ring.find_one(
                {sd_start_key: src_point[sd_id_key],
                 sd_end_key: dst_point[sd_id_key]})
            rt = ring_total.find_one(
                {sd_id_key: src_point[sd_id_key],
                 ring_key: r[ring_key]})

            fraction_before_ring = 1.0 - \
                math.exp(-src_point[selectivity_key] * (rt[to_ring_total_key]) / 1000000.0)

            fraction_after_ring = 1.0 - \
                math.exp(-src_point[selectivity_key] * (
                    rt[to_ring_total_key] + rt[in_ring_total_key]) / 1000000.0)

            quantity_for_ring =\
                src_point[sources_key] * (fraction_after_ring - fraction_before_ring)

            quantity_for_dest = quantity_for_ring *\
                dst_point[destinations_key] / rt[in_ring_total_key]

            me.append({
                sd_start_key: src_point[sd_id_key],
                sd_end_key: dst_point[sd_id_key],
                motion_quantity_key: quantity_for_dest
            })
        motion_exchange.insert_many(me)
    pbar.finish()

if __name__ == "__main__":
    make_motion_exchange()
