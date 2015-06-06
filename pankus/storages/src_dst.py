#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import src_dst_name,sd_id_key

"""Storage for src_dst

Module creates object for database collection connection

data:
    sd_id - point id (indexed field) {0..Z}
    src - sources quantity  {float}
    dst - destination quantity  {float}
    sel - selectivity in parts per million (legacy reasons)

"""

src_dst = MongoCollectionStorageFactory(src_dst_name, [sd_id_key])
