#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory

"""Storage for connection

Module creates object for database collection connection

data:
    weight - weight of connection line produces
    s - start point id (indexed field)
    e - end point id (indexed field)

"""

connection = MongoCollectionStorageFactory(connection_name,[start_key,end_key])