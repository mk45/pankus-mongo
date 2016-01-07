#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pankus.storages.motion_exchange_withdrawal_excess import motion_exchange_withdrawal_excess
from pankus.storages.src_dst import src_dst
from pankus.storages.sd_point import sd_point

from pankus.storages.ring import ring
from pankus.helpers.ram_collection import RamCollection
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import ring_key,sd_id_key,sd_start_key,\
    sd_end_key,motion_quantity_key,destinations_key
import csv


def export_withdrawn_excess():

    ram_src_dst=RamCollection(src_dst)
    ram_motion_exchange_withdrawal_excess=RamCollection(motion_exchange_withdrawal_excess)
    ram_ring=RamCollection(ring,[sd_start_key,sd_end_key])
    ram_sd_point=RamCollection(sd_point,[sd_id_key])

    output=[]
    pbar = Pbar('exporting: ',ram_src_dst.count())
    for region_start in ram_src_dst.find():
        pbar.plus_one()
        for region_end in ram_src_dst.find():

            output.append({

                sd_start_key:region_start[sd_id_key],
                sd_end_key:region_end[sd_id_key],
                motion_quantity_key:ram_motion_exchange_withdrawal_excess.find_one({
                    sd_start_key:region_start[sd_id_key],
                    sd_end_key:region_end[sd_id_key]
                })[motion_quantity_key],
                ring_key:ram_ring.find_one({
                    sd_start_key:region_start[sd_id_key],
                    sd_end_key:region_end[sd_id_key]
                })[ring_key],
                destinations_key:ram_sd_point.find_one({
                    sd_id_key:region_end[sd_id_key]
                })[destinations_key]
            })
    fieldnames=[sd_start_key,sd_end_key,ring_key,destinations_key,motion_quantity_key]
    with open('out_we_mx.csv','wb') as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for element in output:
            writer.writerow(element)

    pbar.finish()
