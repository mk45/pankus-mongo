#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory

"""Storage for stress

Module creates object for database collection connection

data:
    weight - weight of connection line produces
    s - start point id (indexed field)
    e - end point id (indexed field)
    sd_s - start sd point id (indexed field)
    sd_e - end sd point id (indexed field)
    str - stress info {float}
    jun - junction info [id_end:{float},id_end:{float},...]
    itr - interlace info [id_start:[id_end:{float},id_end:{float},...],id_start:...]

"""

stress = MongoCollectionStorageFactory(stress_name, [
    start_key, end_key, sd_start_key, sd_end_key])
