#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import \
    start_key, end_key,turn_info_name


"""Storage for stress

Module creates object for database collection connection

data:
    s - start point id (indexed field)
    e - end point id (indexed field)
    ordered_predecessors - predecessors list
    ordered_successors - successors list

"""

turn_info = MongoCollectionStorageFactory(turn_info_name, [start_key,end_key])
