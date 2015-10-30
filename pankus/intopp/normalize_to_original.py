#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.motion_exchange import motion_exchange
from pankus.storages.sd_point import sd_point
from pankus.storages.src_dst import src_dst
from pankus.helpers.pbar import Pbar


def normalize_to_original():
    src_total = sum([sd[sources_key] for sd in sd_point.find()])
    new_motion_exchange = []
    motion_exchange_total = sum([me[motion_quantity_key] for me in motion_exchange.find()])
    print motion_exchange_total,src_total
    assert motion_exchange_total<src_total*1.01
    pbar = Pbar('normalization: ',motion_exchange.count())

    for me in motion_exchange.find():
        pbar.plus_one()

        new_motion_exchange.append({
            sd_start_key: me[sd_start_key],
            sd_end_key: me[sd_end_key],
            motion_quantity_key: me[motion_quantity_key] * src_total / motion_exchange_total
        })

    motion_exchange.delete_many({})
    motion_exchange.insert_many(new_motion_exchange)
    pbar.finish()

if __name__ == "__main__":
    normalize_to_original()
