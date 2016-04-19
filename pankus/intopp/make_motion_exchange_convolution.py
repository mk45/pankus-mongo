#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.ring import ring
from pankus.storages.ring_total import ring_total
from pankus.storages.src_dst import src_dst
from pankus.storages.motion_exchange_convolution import motion_exchange_convolution
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection
from pankus.defaults.config import \
    sd_id_key,sd_start_key,sd_end_key,ring_key,to_ring_total_key,\
    in_ring_total_key,selectivity_key,sources_key,destinations_key,motion_quantity_key,\
    convolution_a_key,convolution_b_key,convolution_alpha_key
import math

def convolution_cdf(sources,selectivity,conv_a,conv_b):

    if sources<=conv_a:
        return 1.0 - math.exp(-selectivity*sources)

    const = 1.0 - math.exp(-selectivity*conv_a)
    #print "c1",const
    if sources>conv_a and sources<=conv_b+conv_a:
        return const+(math.exp(-selectivity*(conv_a+sources))*\
                     (math.exp(selectivity*sources)*\
                      ((-conv_a*selectivity)+(sources*selectivity)-1.0)+\
                      math.exp(conv_a*selectivity)))/(conv_b*selectivity)

    const=const+(math.exp(-selectivity*(conv_a+(conv_a+conv_b)))*\
                     (math.exp(selectivity*(conv_a+conv_b))*\
                      ((-conv_a*selectivity)+((conv_a+conv_b)*selectivity)-1.0)+\
                      math.exp(conv_a*selectivity)))/(conv_b*selectivity)
    #print "c2",const
    return const+((1.0-math.exp(conv_b*selectivity))*\
                math.exp(-selectivity*(conv_a+conv_b+sources))*\
                (math.exp(selectivity*(conv_a+conv_b))-
                 math.exp(selectivity*sources)))/(conv_b*selectivity)

def make_motion_exchange_convolution():
    """
    Makes motion exchange for intervening opportunities model with convolution
    simple one pre-step of intervening opportunities iteration
    simple but with idea core
    """
    pbar = Pbar('make motion exchange with convolution: ',src_dst.count())
    motion_exchange_convolution.delete_many({})

    ram_src_dst=RamCollection(src_dst)
    ram_ring=RamCollection(ring,[sd_start_key,sd_end_key])
    ram_ring_total=RamCollection(ring_total)

    for src_point in ram_src_dst.find():
        pbar.plus_one()
        me = []
        # data must be present
        assert convolution_a_key in src_point
        assert convolution_b_key in src_point
        #assert convolution_alpha_key in src_point

        for dst_point in ram_src_dst.find():
            r = ram_ring.find_one(
                {sd_start_key: src_point[sd_id_key],
                 sd_end_key: dst_point[sd_id_key]})
            rt = ram_ring_total.find_one(
                {sd_id_key: src_point[sd_id_key],
                 ring_key: r[ring_key]})


            fraction_before_ring = \
                convolution_cdf(
                    rt[to_ring_total_key],
                    src_point[selectivity_key]/1000000.0,
                    src_point[convolution_a_key],
                    src_point[convolution_b_key]
                )

            fraction_after_ring = \
                convolution_cdf(
                    rt[to_ring_total_key]+rt[in_ring_total_key],
                    src_point[selectivity_key]/1000000.0,
                    src_point[convolution_a_key],
                    src_point[convolution_b_key]
                )
            quantity_for_ring =\
                src_point[sources_key] * (fraction_after_ring - fraction_before_ring)

            if rt[in_ring_total_key]!=0:
                quantity_for_dest = quantity_for_ring *\
                    dst_point[destinations_key] / rt[in_ring_total_key]
            else:
                quantity_for_dest = 0

            me.append({
                sd_start_key: src_point[sd_id_key],
                sd_end_key: dst_point[sd_id_key],
                motion_quantity_key: quantity_for_dest
            })
        motion_exchange_convolution.insert_many(me)
    pbar.finish()

if __name__ == "__main__":
    make_motion_exchange()
