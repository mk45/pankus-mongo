#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import \
    sd_start_key,sd_end_key,motion_exchange_name

"""Storage for ring

Module creates object for database collection connection

data:
    sd_s - startnode id (indexed field) {0..Z}
    sd_e - endnode id (indexed field) {0..Z}
    q - quantity of motion (contact volume) between points
"""

motion_exchange = MongoCollectionStorageFactory(motion_exchange_name,[sd_start_key,sd_end_key])