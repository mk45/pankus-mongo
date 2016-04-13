#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.storages.src_dst import src_dst
from pankus.storages.motion_exchange_convolution import motion_exchange_convolution
from pankus.storages.motion_exchange import motion_exchange
from pankus.helpers.pbar import Pbar
from pankus.helpers.ram_collection import RamCollection
from pankus.defaults.config import \
    sd_id_key,sd_start_key,sd_end_key,motion_quantity_key,convolution_alpha_key

def make_convolution_mix(alpha=None):
    """
    Makes mixed model mixes intervening opportunities model with convolution
    or just rewrites convolution model to motion exchange
    """
    pbar = Pbar('mixing models: ',src_dst.count())
    #
    ram_motion_exchange=RamCollection(motion_exchange)
    ram_motion_exchange_convolution=RamCollection(motion_exchange_convolution)
    ram_src_dst=RamCollection(src_dst)
    me = []

    for src_point in ram_src_dst.find():
        pbar.plus_one()
        for dst_point in ram_src_dst.find():

            motion_exchange_quantity=ram_motion_exchange.find_one({
                sd_start_key: src_point[sd_id_key],
                sd_end_key: dst_point[sd_id_key]
            })[motion_quantity_key]
            motion_exchange_conv_quantity=ram_motion_exchange_convolution.find_one({
                sd_start_key: src_point[sd_id_key],
                sd_end_key: dst_point[sd_id_key]
            })[motion_quantity_key]

            if alpha:
                assert alpha>0.0
                assert alpha<1.0
                scale=alpha
            else:
                assert convolution_alpha_key in src_point
                scale=float(src_point[convolution_alpha_key])

            me.append({
                sd_start_key: src_point[sd_id_key],
                sd_end_key: dst_point[sd_id_key],
                motion_quantity_key:
                    (1.0-scale)*motion_exchange_quantity+scale*motion_exchange_conv_quantity
            })


        motion_exchange.delete_many({})
        motion_exchange.insert_many(me)
    pbar.finish()

if __name__ == "__main__":
    make_convolution_mix()
