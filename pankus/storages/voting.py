#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.database.mongo_collection import MongoCollectionStorageFactory

"""Storage for voting

Module creates object for database collection connection

data:
    sd_s - startnode id node who votes (indexed field) {0..Z}
    sd_e - endnode id who is voted(indexed field) {0..Z}
    satisfied_destinations - quantity of vote (contact volume) between points
    destinatins - destinations in voted
    in_ring_total
    to_ring_total
    ring


"""

voting = MongoCollectionStorageFactory(voting_table_name,[sd_start_key,sd_end_key])