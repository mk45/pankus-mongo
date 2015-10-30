#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory

"""Storage for path

data:
    s - start point id (indexed field)
    e - end point id (indexed field)
    w - connection weight {float}
    path - [{0..V},]
    delta - delta weight from shortest
"""


path = MongoCollectionStorageFactory(path_name,[start_key,end_key])
