#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.ring import ring
from pankus.storages.ring_total import ring_total
from pankus.storages.src_dst import src_dst
from pankus.storages.sd_point import sd_point
from pankus.storages.motion_exchange import motion_exchange
from pankus.storages.motion_exchange_withdrawal_excess import motion_exchange_withdrawal_excess
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection
from pankus.intopp.make_motion_exchange import make_motion_exchange
from pankus.defaults.config import \
    sd_id_key,sd_start_key,sd_end_key,ring_key,to_ring_total_key,\
    in_ring_total_key,selectivity_key,sources_key,destinations_key,motion_quantity_key
import math


def make_withdrawal_excess():
    """
    Makes motion exchange wthdraws excess and than do it again
    """

    pbar = Pbar('make withdraw excess: ',3*src_dst.count())

    ram_src_dst=RamCollection(src_dst)
    ram_motion_exchange=RamCollection(motion_exchange)
    ram_motion_exchange_withdrawal_excess=RamCollection(motion_exchange_withdrawal_excess)

    sum_destinations=sum([sd[destinations_key] for sd in ram_src_dst.find()])
    sum_sources=sum([sd[sources_key] for sd in ram_src_dst.find()])
    print sum_destinations,sum_sources

    # we have to proceed only if sources total and destinations total are relatively close (equal)
    if float(sum_destinations)/sum_sources>1.01 or float(sum_destinations)/sum_sources<0.99:
        print "Difference between src and dst over one percent! Exiting."
        pbar.finish()
        return


    realized_percentage_key="realized_percentage"
    inside_realized_motion_key="inside_realized_motion"
    excess_rate_key = "excess"
    #new_dst_key="new_dst"
    #new_src_key="new_src"

    # motion realized by region
    # motion realized in region
    for region in ram_src_dst.find():
        pbar.plus_one()
        region[realized_percentage_key]=1-math.exp(-region[selectivity_key]*sum_destinations/1000000)
        region[inside_realized_motion_key]=sum(mx[motion_quantity_key] for mx in ram_motion_exchange.find({
            sd_end_key:region[sd_id_key]
          }))
        #region[new_src_key]=region[sources_key]


    # fraction of realized motion
    sum_realized=sum([mx[motion_quantity_key] for mx in ram_motion_exchange.find()])
    realized_fraction=(sum_realized/sum_sources)
 
    for region in ram_src_dst.find():
        pbar.plus_one()
        #one over excess fraction - how to scale (lower) motion
        region[excess_rate_key]=region[inside_realized_motion_key]\
            /(region[destinations_key]*realized_fraction)
        if region[excess_rate_key]>1:
            for mx in ram_motion_exchange.find({
                    sd_end_key:region[sd_id_key]
                }):
                motion_that_should_be=mx[motion_quantity_key]/region[excess_rate_key]
                mx[motion_quantity_key]=motion_that_should_be

    for region in ram_src_dst.find():
        pbar.plus_one()
        region[sources_key]=region[sources_key]-\
                                sum([mx[motion_quantity_key] for mx in ram_motion_exchange.find({
                                    sd_start_key:region[sd_id_key]
                                })])
        region[destinations_key]=region[destinations_key]-\
                                sum([mx[motion_quantity_key] for mx in ram_motion_exchange.find({
                                    sd_end_key:region[sd_id_key]
                                })])

    sum_new_destinations=sum([region[destinations_key] for region in ram_src_dst.find()])

    # set new selectivity new dst new src
    for region in ram_src_dst.find():
        region[selectivity_key]=\
            ((-math.log(1-region[realized_percentage_key])*1000000)/sum_new_destinations)


    # update withdrawal table
    if ram_motion_exchange_withdrawal_excess.count()!=0:
        for mx in ram_motion_exchange.find():
            ram_motion_exchange_withdrawal_excess.find_one({
                sd_start_key:mx[sd_start_key],
                sd_end_key:mx[sd_end_key]
            })[motion_quantity_key]+=mx[motion_quantity_key]
        motion_exchange_withdrawal_excess.delete_many({})
        motion_exchange_withdrawal_excess.insert_many(ram_motion_exchange.find())
    else:
        motion_exchange_withdrawal_excess.insert_many(ram_motion_exchange.find())

    src_dst.delete_many({})
    src_dst.insert_many(ram_src_dst.find())

    motion_exchange.delete_many({})
    motion_exchange.insert_many(ram_motion_exchange.find())

    pbar.finish()

if __name__ == "__main__":
    make_motion_exchange()
