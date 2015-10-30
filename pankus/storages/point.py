#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory

"""Storage for point

data
    id (indexed) - id of point {0..N}
    p - point geometry [x, y]
"""


point = MongoCollectionStorageFactory(point_name, [id_key])
