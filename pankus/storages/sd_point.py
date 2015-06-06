#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import sd_id_key,point_key

"""Storage for sd_point

Module creates object for database collection connection

data:
    sd_id - point id (indexed field) {0..Z}
    p - point coordinates point geometry (indexed field) [x, y]
    src - sources quantity (non mandatory) {float}
    dst - destination quantity (non mandatory) {float}
    sel - source selectivity (non mandatory)

"""

sd_point = MongoCollectionStorageFactory('sd_point', [sd_id_key, point_key])
