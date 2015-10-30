#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.default_config import default_config
"""Storage for crs (coordinate reference system)

data:
    project config data : one data row

"""

config = MongoCollectionStorageFactory(default_config['config_name'],[])