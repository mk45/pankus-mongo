#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory


"""Storage for featured_point

Module creates object for database collection connection

data:
    id - point id (indexed field) {0..N}
    sd_id - sd_point id (indexed field) {0..Z}
    p - point coordinates

"""

featured_point = MongoCollectionStorageFactory(featured_point_name,[sd_id_key,id_key])