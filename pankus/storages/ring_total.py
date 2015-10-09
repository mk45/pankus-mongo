#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory
from pankus.defaults.config import \
    sd_id_key,ring_total_name,ring_key

"""Storage for ring_total

Module creates object for database collection connection

data:
    sd_id - startnode id (indexed field) {0..Z}
    r - ring number  (indexed field)
    in_ring_total - total destinations in this ring
    to_ring_total - total destinations in previous rings
    points_in_ring - all points number in this rings
"""

ring_total = MongoCollectionStorageFactory(ring_total_name,[sd_id_key,ring_key])