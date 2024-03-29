#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pymongo import MongoClient

from pankus.defaults.config import default_database as db_name


class MongoCollectionStorageFactory(object):

    def __init__(self, name, indexes):
        coll = MongoClient()[db_name][name]
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

        self.insert_one = coll.insert_one
        self.insert_many = coll.insert_many
        self.count = coll.count

        self.update_one = coll.update_one
        self.update_many = coll.update_many

    def finish(self):
        pass
