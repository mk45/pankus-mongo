#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.helpers.pbar import Pbar
from pankus.storages.sd_point import sd_point
from pankus.storages.src_dst import src_dst
from pankus.storages.ring import ring
#from pankus.storages.featured_point import featured_point
from pankus.helpers.ram_collection import RamCollection
from pankus.defaults.config import \
    sd_id_key,sources_key,destinations_key,selectivity_key,sd_start_key,sd_end_key,ring_key
import argparse


def get_ring_for_sd_point(sd_id,attribute_name):

    pbar = Pbar('saving ring info:  ',src_dst.count())

    assert sd_point.find_one({sd_id_key:sd_id})

    ram_sd_point=RamCollection(sd_point,[sd_id_key])

    for rings_of_interest in ring.find({sd_start_key: sd_id}):
        pbar.plus_one()
        sd_p=ram_sd_point.find_one({sd_id_key: rings_of_interest[sd_end_key]})
        sd_p[attribute_name]=rings_of_interest[ring_key]

    sd_point.delete_many({})
    sd_point.insert_many(ram_sd_point.find({}))
    pbar.finish()