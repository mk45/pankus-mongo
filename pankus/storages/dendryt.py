#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import \
    start_key,end_key,dendryt_name

"""Storage for dendryt

Module creates object for database collection connection

data:
    s - startnode id (indexed field) {0..Z}
    e - endnode id (indexed field) {0..V}
    w - connection weight {float}
    x - successor of s on s to e path id {0..V}
    y - predeccssor of e on s to e path id {0..V}

"""

dendryt = MongoCollectionStorageFactory(dendryt_name,[start_key,end_key])