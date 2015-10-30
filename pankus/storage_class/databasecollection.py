#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.defaults.default_config import default_config
from pymongo import MongoClient


class DatabaseCollection(object):

    def __init__(self,name):
        assert isinstance(name , str)
        self.config=default_config
        self.database=MongoClient()[self.config['default_database']]
        self.collection=self.database[name]

    def add_field(self,name,type):
        # in mongodb adding fields is lazy
        assert isinstance(name , str)
        pass

    def add_index(self,name):
        assert isinstance(name , str)
        self.collection.create_index(name)

    def find(self,search_dict):
        return self.collection.find(search_dict)

    def find_one(self,search_dict):
        return self.collection.find_one(search_dict)

    def insert_one(self,value):
        self.collection.insert_one(value)

    def insert_many(self,values):
        self.collection.insert_many(values)

    def delete_many(self,search_dict):
        self.collection.delete_many(search_dict)

    def count(self):
        return self.collection.count()

    def commit(self):
        pass