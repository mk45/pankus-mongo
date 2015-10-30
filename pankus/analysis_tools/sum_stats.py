#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from math import sqrt
from pankus.storages.src_dst import src_dst
from pankus.storages.sd_point import sd_point
from pankus.storages.motion_exchange import motion_exchange
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection


def sum_stats(in_sd_point_sum_name):

    ram_motion_exchange=RamCollection(motion_exchange)
    #pbar = Pbar('make analysis',src_dst.count())
    sd_list =[point for point in src_dst.find()]
    mx_list =[mx for mx in motion_exchange.find() ]
    sources_total = sum([point[sources_key] for point in sd_list])
    destinations_total = sum([point[destinations_key] for point in sd_list])
    motions_total=sum([motion[motion_quantity_key] for motion in mx_list])

    pbar = Pbar('saving: ',sd_point.count())
    ram_sd_point=RamCollection(sd_point,[sd_id_key])
    assigned_dst_diffs=[]
    for sd in ram_sd_point.find():
        pbar.plus_one()
        sd_id=sd[sd_id_key]

        #sd_p=ram_sd_point.find_one({sd_id_key: sd[sd_id_key]})
        sd[in_sd_point_sum_name]=\
            sum([mx[motion_quantity_key] for mx in ram_motion_exchange.find({
                sd_end_key:sd_id
            })])
        assigned_dst_diffs.append(sd[in_sd_point_sum_name]-sd[destinations_key])

    sd_point.delete_many({})
    sd_point.insert_many(ram_sd_point.find())
    pbar.finish()

    print "sources total", sources_total
    print "destinations total", destinations_total
    print "motions realized",motions_total
    print "realized fraction",motions_total/destinations_total
    print "low end realization",min(assigned_dst_diffs)
    print "high end realization",max(assigned_dst_diffs)
    print "assign and reality distance:", sqrt(sum(a**2 for a in assigned_dst_diffs))

    #pbar.finish()
