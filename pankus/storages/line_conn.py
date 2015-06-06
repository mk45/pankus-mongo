#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import start_key,end_key,line_conn_name

"""Storage for line_conn

Module creates object for database collection connection

data:
    linestring - geometry of line [[x, y],....]
    weight - weight of connection line produces
    s - start point id (indexed field)
    e - end point id (indexed field)
    throughput: - throughput of connection
    strs - stress on edge (in output)
    junc - edges end junction situation (in output)
    intl - interlace situation on edge (in output)
    ...


"""

line_conn = MongoCollectionStorageFactory(line_conn_name,[start_key,end_key])