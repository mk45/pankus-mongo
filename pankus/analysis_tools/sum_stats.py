#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from math import sqrt
from pankus.storages.src_dst import src_dst
from pankus.storages.sd_point import sd_point
from pankus.storages.motion_exchange import motion_exchange
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection
from pankus.defaults.config import sources_key,destinations_key,motion_quantity_key,\
    sd_id_key,sd_end_key



def sum_stats(to_sd_point_motion_sum_name=None):

    #pbar = Pbar('make analysis',src_dst.count())

    pbar = Pbar('get statistics: ',sd_point.count())
    ram_motion_exchange=RamCollection(motion_exchange)

    motions_total=sum([motion[motion_quantity_key] for motion in ram_motion_exchange.find()])

    ram_sd_point=RamCollection(sd_point,[sd_id_key])
    sources_total = sum([point[sources_key] for point in ram_sd_point.find()])
    destinations_total = sum([point[destinations_key] for point in ram_sd_point.find()])

    assigned_dst_diffs=[]

    for sd in ram_sd_point.find():
        pbar.plus_one()
        sd_id=sd[sd_id_key]
        total_to_sd_motion=\
            sum([mx[motion_quantity_key] for mx in ram_motion_exchange.find({
                sd_end_key:sd_id
            })])
        assigned_dst_diffs.append(total_to_sd_motion-sd[destinations_key])

        if to_sd_point_motion_sum_name:
            sd[to_sd_point_motion_sum_name]=total_to_sd_motion

    if to_sd_point_motion_sum_name:
        sd_point.delete_many({})
        sd_point.insert_many(ram_sd_point.find())
    pbar.finish()

    print "sources total", sources_total
    print "destinations total", destinations_total
    print "motions realized",motions_total
    print "realized fraction",motions_total/destinations_total
    print "lowest realization",min(assigned_dst_diffs)
    print "highest realization",max(assigned_dst_diffs)
    print "assign and reality distance:", sqrt(sum(a**2 for a in assigned_dst_diffs))/\
                                          sqrt(sum([b[destinations_key]**2 for b  in ram_sd_point.find({})]))


