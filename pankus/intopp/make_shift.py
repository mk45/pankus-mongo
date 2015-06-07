#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pankus.storages.src_dst import src_dst
from pankus.storages.motion_exchange import motion_exchange
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    sources_key, destinations_key,motion_quantity_key,\
    sd_end_key,sd_id_key,selectivity_key


def make_shift(shift_type):
    src_total = sum([sd[sources_key] for sd in src_dst.find()])
    dst_total = sum([sd[destinations_key] for sd in src_dst.find()])

    new_src_dst = []
    pbar = Pbar('make '+shift_type+ ' shift: ',src_dst.count())
    for point in src_dst.find():
        pbar.plus_one()
        to_point_motion_total = sum([
            m[motion_quantity_key] for m in motion_exchange.find({sd_end_key: point[sd_id_key]})
        ])
        if shift_type == 'destinations':
            new_point_dst = to_point_motion_total * dst_total / src_total
            new_point_src = point[sources_key]
        elif shift_type == 'general':
            new_point_dst = to_point_motion_total * dst_total / src_total
            new_point_src = to_point_motion_total
        elif shift_type == 'sources':
            new_point_dst = point[destinations_key]
            new_point_src = to_point_motion_total
        else:
            raise ValueError("What is: "+shift_type)
        new_src_dst.append({
            sd_id_key: point[sd_id_key],
            destinations_key: new_point_dst,
            sources_key: new_point_src,
            selectivity_key: point[selectivity_key]
        })
    src_dst.delete_many()
    src_dst.insert_many(new_src_dst)
    pbar.finish()


def make_sources_shift():
    make_shift('sources')

def make_destinations_shift():
    make_shift('destinations')

def make_general_shift():
    make_shift('general')
