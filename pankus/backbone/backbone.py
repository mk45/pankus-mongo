#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.defaults.default_config import default_config
from pankus.defaults.collections_config import collections_config
import psutil,os
from pymongo import MongoClient
from pankus.helpers.pbar import Pbar

class Backbone(object):

    class TempCollection(list):
        def insert_one(self,element):
            self.append(element)

        def insert_many(self,elements):
            self.extend(elements)

    class ProxyDBCollection(object):
        def __init__(self,coll):
            self.coll=coll
            self.insert_one=coll.insert_one


        def insert_one(self,element):
            self.append(element)

        def insert_many(self,elements):
            self.extend(elements)


    def __init__(self):
        self.config=default_config
        self.database=MongoClient()[self.config['default_database']]
        #self.__load_config_from_db_collection('config')
        self.collections={}
        self.progress_bar=None
        self.generated_collection_name=None
        self.current_collections={}


    def get_config(self,name):
        self.__load_config_from_db_collection(self.config['config'])
        if name in self.config:
            return self.config[name]
        else:
            raise ValueError()

    def __collection_exists(self,name):
        return name in self.database.collection_names()

    def __get_db_collection(self,name):
        assert self.__collection_exists(name)
        return self.database[name]


    def __load_config_from_db_collection(self,name):
        config=self.__get_db_collection(name)
        if config:
            self.config=config.find_one()

    def __create_db_collection(self,name):
        coll = self.database[self.config[name]]
        assert isinstance(collections_config[name]['index'],list)
        for index in collections_config[name]['index']:
            assert isinstance(index, str)
            coll.create_index(index)
        return coll

    def __cache_collection(self):
        pass

    def __can_we_load_it_into_memory(self,elements):
        pass

    def __can_we_remove_something(self):
        pass

    def __free_memory(self):
        pass

    def free_memory_for_tmp_collection(self,estimated_size):
        pass

    def get_collection(self,name):
        """
        :param name:
        :return:
        cashed collection
        """

        if not self.__collection_exists(name):
            self.__create_db_collection(name)



        if self.get_config('cache_enabled'):
            if collections_config[name]['cached'] == 'full':
                pass
            elif collections_config[name]['cached'] == 'partial':
                pass
        else:
            return self.ProxyDBCollection()


    def open_action(self,action_name,generated_collection_name,
                    iteration_size,additional_collection_list=None):
        self.progress_bar=Pbar(action_name,iteration_size)
        self.generated_collection_name=generated_collection_name
        returned_collections={
            generated_collection_name:self.get_collection(generated_collection_name)
        }
        for coll in additional_collection_list:
            assert isinstance(coll,str)
            returned_collections[coll]=self.get_collection(coll)
        return returned_collections


    def iteration(self):
        self.progress_bar.plus_one()

    def close_action(self):
        self.current_collections={}
        self.generated_collection_name=None
        self.progress_bar.finish()




# We make instance for singleton-like behavior
#
backbone=Backbone()