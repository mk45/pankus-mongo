#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.ring import ring
from pankus.storages.ring_total import ring_total
from pankus.storages.src_dst import src_dst
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection

def make_rings_total():
    """
    Counts destinations in rings

    """
    pbar = Pbar('count rings dst: ',src_dst.count())
    ram_ring=RamCollection(ring,[sd_start_key,ring_key])
    ram_src_dst=RamCollection(src_dst,[sd_id_key])
    max_ring = max([r[ring_key] for r in ring.find()])
    new_ring_total=[]
    for point in src_dst.find():
        pbar.plus_one()
        to_ring_total=0
        for ring_number in range(max_ring + 1):
            points_in_ring = [r[sd_end_key] for r in ram_ring.find(
                {sd_start_key: point[sd_id_key],
                 ring_key: ring_number})]

            in_ring_total = sum([ram_src_dst.find_one({sd_id_key: sd_id})[destinations_key]
                                 for sd_id in points_in_ring])

            new_ring_total.append({
                sd_id_key: point[sd_id_key],
                ring_key: ring_number,
                in_ring_total_key: in_ring_total,
                to_ring_total_key: to_ring_total,
                points_in_ring_key:points_in_ring
            })
            to_ring_total=to_ring_total+in_ring_total

    ring_total.delete_many({})
    ring_total.insert_many(new_ring_total)
    pbar.finish()

if __name__ == "__main__":
    make_rings_total()
