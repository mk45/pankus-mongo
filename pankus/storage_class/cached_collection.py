#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storage_class.databasecollection import DatabaseCollection



class Elements(object):
    def __init__(self,real_elements):
        self.index=None
        self.elements=[]

    def find(self,search_dict):
        if search_dict=={}:
            for

class Multielement(Elements):
    def __init__(self):
        pass

class Singleelement(Elements):
    def __init__(self):
        pass

class StartIndexed(Elements):
    def __init__(self,field_name):
        self.field_name=field_name
        self.current_element=None

    def elements_list(self,elements):
    def find(self,search_dict):



class NumberIndex(Elements):
    def __init__(self,field_name):
        self.field_name=field_name
        self.created=False
        self.index=[]
        self.index_inside=None


    def find(self,search_dict):
        if self.field_name not in search_dict:
            return []
        else:
            new_search=dict(search_dict)
            del(new_search[self.field_name])
            return self.index[search_dict[self.field_name]].find(new_search)

    def insert(self,element):
        if self.index_inside:
            pass
        else:
            pass

    def create(self,search_dict,collection):
        if self.created:
            self.index[search_dict[self.field_name]].find(search_dict)
        else:
            for element in collection.find({}):
                self.insert(element)
    def insert_element(self,element):
        pass

class DictIndex(Elements):
    def __init__(self,field_name):
        self.field_name=field_name

    def find(self,search_dict):

        if self.field_name not in search_dict:
            return []
        else:
            new_search=dict(search_dict)
            del(new_search[self.field_name])
            return self.index[search_dict[self.field_name]].find(new_search)

    def insert(self):
        pass


class Storage(DatabaseCollection):

    def __init__(self,name):
        super(Storage,self).__init__(name)
        self.fields={}
        # initial estiation of element size
        #self.elements_count=elements_count
        self.collection=super(Storage,self)
        self.index=None
        self.dirty=None
        self.caching_enabled=False
        #index

        #self.index=None

            # set idxs
        # get config about caching
        if True:

            pass
        else:

            # use slow but reliable method through database
            # find_one , find , insert_many , insert_one are inherited


    def add_field(self,name,type):
        self.fields[name]=type

        super(Storage,self).add_field(name,type)

    def add_index(self,index_object):
        if isinstance(index_object,str):
            self.caching_enabled=False
            super(Storage,self).add_index(index_object)
        else:
            assert isinstance(index_object,StartIndexed) or\
                    isinstance(index_object,NumberIndex) or\
                    isinstance(index_object,DictIndex)
            super(Storage,self).add_index(index_object.field_name)

            if not self.index:
                self.index=index_object
            else:
                self.index.inner_index(index_object)

    def commit(self):
        self.index.commit()

    def can_caching_be_used(self):
        return self.caching_enabled

    def find(self,search_dict):
        if self.can_caching_be_used():
            self.index.create(search_dict,self.collection)
            return self.index.find(search_dict)
        else:
            return self.index.find(search_dict)

    def find_one(self,search_dict):
        return self.index.find_one(search_dict)

    def delete_many(self,search_dict):
        return self.index.delete_many(search_dict)

    def insert_
