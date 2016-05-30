#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pankus.storages.src_dst import src_dst
from pankus.storages.ring import ring
from pankus.storages.ring_total import ring_total
from pankus.helpers.ram_collection import RamCollection
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import ring_key,sd_id_key,sd_start_key,\
    sd_end_key,destinations_key,convolution_contribution,to_ring_total_key,\
    in_ring_total_key,convolution_a_key,convolution_b_key,convolution_alpha_key
import csv


def export_convolution_contribution():

    ram_src_dst=RamCollection(src_dst)
    ram_ring=RamCollection(ring,[sd_start_key,ring_key])
    ram_ring_total=RamCollection(ring_total,[sd_id_key,ring_key])
    max_ring = max([r[ring_key] for r in ram_ring.find()])


    output=[]
    pbar = Pbar('exporting: ',ram_src_dst.count())

    for region_start in ram_src_dst.find():
        pbar.plus_one()

        for ring_number in range(max_ring + 1):

            ring_total_info=ram_ring_total.find_one({
                sd_id_key:region_start[sd_id_key],
                ring_key:ring_number
            })

            if not ring_total_info:
                continue

            contribution=0.0
            conv_a=region_start[convolution_a_key]
            conv_size=region_start[convolution_b_key]
            conv_end=conv_a+conv_size
            ring_start=ring_total_info[to_ring_total_key]
            ring_size=ring_total_info[in_ring_total_key]
            ring_end=ring_start+ring_size

            # convolution inside ring
            if ring_start < conv_a and ring_end > conv_end:
                contribution=conv_size

            # convolution begins in ring
            elif ring_start <= conv_a and ring_end > conv_a and ring_end <= conv_end:
                contribution=ring_end-conv_a

            #convolution ends in ring
            elif ring_start < conv_end and ring_end >= conv_end:
                contribution=conv_end-ring_start

            #convolution spans over ring
            elif ring_start > conv_a and ring_end < conv_end:
                contribution=ring_size
            else:
                contribution=0.0

            # for negative conv_a convolutions spans over ring
            if conv_a<0 and ring_end <= -conv_a:
                contribution+=ring_size

            # for negative conv_a convolutions starts in ring
            elif conv_a<0 and ring_end > -conv_a and ring_start < -conv_a:
                contribution+=-conv_a-ring_start
            else:
                pass

            for region_end in ram_ring.find({
                sd_start_key:region_start[sd_id_key],
                ring_key:ring_number
            }):
                output.append({

                    sd_start_key:region_start[sd_id_key],
                    sd_end_key:region_end[sd_end_key],
                    convolution_contribution:contribution/ring_size * region_start[convolution_alpha_key]
                })

    fieldnames=[sd_id_key,convolution_contribution]
    with open('convolution_contribution.csv','wb') as f:
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        for element in output:
            writer.writerow(element)

    pbar.finish()
