#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pymongo import MongoClient
from pankus.defaults.default_config import default_config

class MongoCollectionStorageFactory(object):

    def __init__(self, name, indexes):
        default_database=default_config['default_database']
        coll = MongoClient()[default_database][name]
        self.coll = coll
        self.name = name
        self.indexes = indexes
        assert isinstance(indexes, list)
        for index in indexes:
            assert isinstance(index, str)
            coll.create_index(index)

        self.find = coll.find
        self.find_one = coll.find_one
        #self.drop = coll.drop
        self.delete_many = coll.delete_many

        #self.insert_one = coll.insert_one
        self.insert_many = coll.insert_many
        self.count = coll.count

        #self.update_one = coll.update_one
        #self.update_many = coll.update_many

    def finish(self):
        pass
