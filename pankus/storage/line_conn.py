#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import start_key,end_key

"""Storage for line_conn

Module creates object for database collection connection

data:
    linestring - geometry of line [[x, y],....]
    weight - weight of connection line produces
    s - start point id (indexed field)
    e - end point id (indexed field)
    throughput: - throughput of connection
    outputs:
        strs
        junc
        intl
    ...


"""

line_conn = MongoCollectionStorageFactory('line_conn',[start_key,end_key])