#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import \
    sd_start_key,sd_end_key,ring_key,ring_name

"""Storage for ring

Module creates object for database collection connection

data:
    sd_s - startnode id (indexed field) {0..Z}
    sd_e - endnode id (indexed field) {0..Z}
    r - ring number  (indexed field)
"""

ring = MongoCollectionStorageFactory(ring_name,[sd_start_key,sd_end_key,ring_key])