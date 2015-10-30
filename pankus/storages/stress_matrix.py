#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory


"""Storage for stress

Module creates object for database collection connection

data:
    s - start point id (indexed field)
    e - end point id (indexed field)
    q - quantity of applied stress {float}
"""

stress_matrix = MongoCollectionStorageFactory(stress_matrix_name, [start_key,end_key])
