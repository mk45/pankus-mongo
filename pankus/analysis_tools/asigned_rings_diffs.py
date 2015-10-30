#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from math import exp
from pankus.storages.src_dst import src_dst
from pankus.storages.motion_exchange import motion_exchange
from pankus.storages.ring import ring
from pankus.storages.ring_total import ring_total
from pankus.storages.sd_to_ring_motion import sd_to_ring_motion
from pankus.storages.voting import voting
from pankus.helpers.ram_collection import RamCollection
from pankus.helpers.pbar import Pbar
import pankus.defaults.config

def assigned_rings_diffs(satisfaction_level=0.99):
    #src_total = sum([sd[sources_key] for sd in src_dst.find()])
    #dst_total = sum([sd[destinations_key] for sd in src_dst.find()])
    max_ring = max([r[ring_key] for r in ring.find()])

    new_sd_to_ring_motion = []
    new_vote=[]
    ram_ring_total=RamCollection(ring_total)
    ram_motion_exchange=RamCollection(motion_exchange)
    ram_src_dst=RamCollection(src_dst)

    pbar = Pbar('make analysis',src_dst.count())
    for point in ram_src_dst.find():
        pbar.plus_one()

        for ring_number in range(max_ring + 1):

            ring_info=ram_ring_total.find_one({
                sd_id_key: point[sd_id_key],
                ring_key: ring_number
            })

            points_in_ring = ring_info[points_in_ring_key]

            in_ring_destinations=ring_info[in_ring_total_key]

            to_ring_destinations=ring_info[to_ring_total_key]

            to_ring_motion_from_source = sum([
                ram_motion_exchange.find_one({
                    sd_end_key:key,
                    sd_start_key:point[sd_id_key]
                })[motion_quantity_key]
                for key in points_in_ring
            ])

            to_ring_motion_total = sum([
                sum([mx[motion_quantity_key]
                     for mx in  ram_motion_exchange.find({
                        sd_end_key:key
                        })
                ])
                for key in points_in_ring
            ])

            if to_ring_destinations*point[selectivity_key]/1000000.0<1.0:
                near=1
            #elif to_ring_destinations*\
            #    point[selectivity_key]/1000000.0>1.0:
            #    near=-1
            else:
                near = 0

            if in_ring_destinations >0:
                in_ring_realized_fraction=\
                    to_ring_motion_total/(in_ring_destinations*satisfaction_level)

                new_sd_to_ring_motion.append({
                    sd_id_key: point[sd_id_key],
                    ring_key: ring_number,
                    sources_key: point[sources_key],
                    selectivity_key: point[selectivity_key],
                    to_ring_motion_key: to_ring_motion_from_source,
                    in_ring_total_key: in_ring_destinations,
                    satisfied_destinations_part_key:in_ring_realized_fraction,
                    "DET1":near,
                    # "DET2":to_ring_motion_from_source*
                    #        exp(-(point[selectivity_key]*(to_ring_destinations+in_ring_destinations)))*
                    #        (1-in_ring_realized_fraction)
                })



                for p in points_in_ring:

                    p_dst=ram_src_dst.find_one({
                        sd_id_key:p
                    })[destinations_key]

                    to_point_motion_total=sum([
                        mx[motion_quantity_key]
                        for mx in ram_motion_exchange.find({
                            sd_end_key:p
                        })
                    ])

                    points_exchange=ram_motion_exchange.find_one({
                        sd_start_key:point[sd_id_key],
                        sd_end_key:p
                    })[motion_quantity_key]

                    motions_surplus=to_point_motion_total-p_dst


                    new_vote.append({
                        sd_end_key:point[sd_id_key],
                        sd_start_key:p,
                        satisfied_destinations_part_key:in_ring_realized_fraction,
                        "ms":motions_surplus,
                        "px":points_exchange,
                        "near":near
                    })

    sd_to_ring_motion.delete_many({})
    sd_to_ring_motion.insert_many(new_sd_to_ring_motion)
    voting.delete_many({})
    voting.insert_many(new_vote)
    pbar.finish()
