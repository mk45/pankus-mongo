#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory

"""Storage for to ring motions from source

Module creates object for database collection connection

data:
    sd_s - startnode id (indexed field) {0..Z}
    r - ring id
    to_ring_motion - quantity of motion (contact volume) to ring
    satisfied_destinations - fraction of satisfied destinations
    ...
"""

sd_to_ring_motion = MongoCollectionStorageFactory(sd_to_ring_motion_name,[sd_start_key,ring_key])