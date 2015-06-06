#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.ring import ring
from pankus.storages.ring_total import ring_total
from pankus.storages.src_dst import src_dst
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    ring_key,sd_end_key,sd_start_key,sd_id_key,destinations_key,in_ring_total_key,to_ring_total_key

def make_rings_total():
    """
    Counts destinations in rings

    """
    pbar = Pbar('count rings dst: ',src_dst.count())
    ring_total.delete_many({})

    max_ring = max([r[ring_key] for r in ring.find()])
    for point in src_dst.find():
        pbar.plus_one()
        for ring_number in range(max_ring + 1):
            points_in_ring = [r[sd_end_key] for r in ring.find(
                {sd_start_key: point[sd_id_key],
                 ring_key: ring_number})]
            in_ring_total = sum([src_dst.find_one({sd_id_key: sd_id})[destinations_key]
                                 for sd_id in points_in_ring])

            if ring_number == 0:
                to_ring_total = 0
            else:
                prev_ring = ring_total.find_one(
                    {sd_id_key: point[sd_id_key],
                     ring_key: ring_number - 1})
                to_ring_total = prev_ring[
                    to_ring_total_key] + prev_ring[in_ring_total_key]

            ring_total.insert_one({
                sd_id_key: point[sd_id_key],
                ring_key: ring_number,
                in_ring_total_key: in_ring_total,
                to_ring_total_key: to_ring_total
            })
    pbar.finish()

if __name__ == "__main__":
    make_rings_total()
