#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from math import log
from pankus.storages.src_dst import src_dst
from pankus.storages.sd_point import sd_point
from pankus.storages.ring_total import ring_total
from pankus.storages.motion_exchange import motion_exchange
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection


def selfsteer_selectivity(satisfaction_level=0.99):
    #assert satisfaction_level<1.0
    new_src_dst = []

    pbar = Pbar('change selectivity: ',src_dst.count())

    #ram_motion_exchange=RamCollection(motion_exchange)
    ram_src_dst=RamCollection(src_dst)
    ram_ring_total=RamCollection(ring_total)
    ram_sd_point=RamCollection(sd_point,[sd_id_key])
    ram_motion_exchange=RamCollection(motion_exchange)

    new_src_dst=[]

    for point in ram_src_dst.find():
        pbar.plus_one()

        ring_info=ram_ring_total.find_one({
                sd_id_key: point[sd_id_key],
                ring_key: 0
            })

        in_ring_destinations=ring_info[in_ring_total_key]

        to_stay=ram_sd_point.find_one({
            sd_id_key:point[sd_id_key]
        })[destinations_key]

        to_self_motion=ram_motion_exchange.find_one({
            sd_start_key:point[sd_id_key],
            sd_end_key:point[sd_id_key]
        })[motion_quantity_key]


        if to_stay<point[destinations_key]*satisfaction_level:
            p=1-(to_self_motion/point[destinations_key])*\
               ((to_stay)/(point[destinations_key]*satisfaction_level))
            #p=1-((to_stay)/(point[destinations_key]*satisfaction_level))

            new_selectivity=-log(p)*(1000000.0/point[destinations_key])/5

        else:
            if point[destinations_key]==0:
                new_selectivity=1
            else:
                new_selectivity=-log(0.00001)*(1000000.0/point[destinations_key])

        #if new_selectivity>100000.0:
        #    new_selectivity=100000.0

        new_src_dst.append({
            sd_id_key: point[sd_id_key],
            destinations_key: point[destinations_key],
            sources_key: point[sources_key],
            selectivity_key: new_selectivity
        })

    src_dst.delete_many({})
    src_dst.insert_many(new_src_dst)
    pbar.finish()
