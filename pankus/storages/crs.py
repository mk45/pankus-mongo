#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory

"""Storage for crs (coordinate reference system)

data:
    contains only one document

"""

crs = MongoCollectionStorageFactory(crs_name,[])