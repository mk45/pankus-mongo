#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storage_class.databasecollection import DatabaseCollection




class RamCache(object):
    """
    Simple Cache without index
    """
    def __init__(self,upper_object):
        super(Index,self).__init__(upper_object)
        self.collection=collection
        self.inner_index=[]

    def insert_one(self,element):
        self.elements.append(element)

    def insert_many(self,elements):
        self.elements.extend(elements)

    def find(self,search_dict):
        if self.have_to_index:
            self.elements=list(self.collection.find())
            self.have_to_index=None

        search_items=search_dict.items()
        for element in self.elements:
            if all([key in element and element[key]==value
                    for key,value in search_items]):
                    yield element

    def find_one(self,search_dict):
        result = self.find(search_dict)
        return result.next()

    def count(self):
        return len(self.elements)

    def delete_many(self,search_dict):
        self.elements=[]


class StartIndexed(object):
    def __init__(self,field_name):
        self.field_name=field_name
        self.current_value=None
        self.inner_index=None
        self.collection=None
        self.fields_under=[]
        self.elements=None

    def insert_one(self,element):
        if self.field_name not in element:
            raise ValueError("element must have indexed field")
        if element[self.field_name]==self.current_value:
            self.inner_index.insert_one(element)

        else:

            if self.fields_under==[]:
                self.collection.insert_many(self.elements)

            self.inner_index.delete_many({})
            self.elements=[]
            self.current_value=element[self.field_name]
            self.inner_index.insert_one(element)

        self.elements.append(element)


    def delete_many(self,search_dict):
        self.current_value=None
        self.inner_index.delete_many(search_dict)

    def insert_many(self,elements):
        for element in elements:
            assert self.field_name in element and element[self.field_name]==self.current_value
            self.inner_index.insert_one(element)

    def find(self,search_dict):
        if self.field_name not in search_dict:
            raise ValueError("element must have indexed field")
        if search_dict[self.field_name]==self.current_value:
            return self.inner_index.find(search_dict)

        self.inner_index.delete_many({})

        # rebuild
        tmp_filter=dict([(k,v) for k,v in sear  ch_dict.items() if k in self.fields_under+[k] ])
        self.inner_index.insert_many(self.collection.find(tmp_filter))

        self.current_value=search_dict[self.field_name]
        self.inner_index.find(search_dict)

    def find_one(self,search_dict):
        result = self.find(search_dict)
        return result.next()

    def add_inner_index(self,index):
        self.inner_index=index
        self.inner_index.collection=self.collection
        self.inner_index.fields_under=list(self.fields_under)
        self.inner_index.fields_under.append(self.field_name)
        self.elements=[]


class NumberIndex(object):
    def __init__(self,field_name):
        self.field_name=field_name
        self.inner_index=None
        self.idx=[]
        self.collection=None
        self.fields_under=[]


    def insert_one(self,element):
        if self.field_name not in element:
            raise ValueError("element must have indexed field")
        while len()
        if element[self.field_name]==self.current_value:
            self.inner_index.insert_one(element)
            # insert to lower instance insert_one(element)
        else:

            if self.fields_under==[]:
                self.collection.

            self.inner_index.delete_many({})
            self.current_value=element[self.field_name]
            self.inner_index.insert_one(element)

    def delete_many(self,search_dict):
        self.current_value=None
        self.inner_index.delete_many(search_dict)

    def insert_many(self,elements):
        for element in elements:
            assert self.field_name in element and element[self.field_name]==self.current_value
            self.inner_index.insert_one(element)

    def find(self,search_dict):
        if self.field_name not in search_dict:
            raise ValueError("element must have indexed field")
        if search_dict[self.field_name]==self.current_value:
            return self.inner_index.find(search_dict)

        self.inner_index.delete_many({})

        # rebuild
        tmp_filter=dict([(k,v) for k,v in sear  ch_dict.items() if k in self.fields_under+[k] ])
        self.inner_index.insert_many(self.collection.find(tmp_filter))

        self.current_value=search_dict[self.field_name]
        self.inner_index.find(search_dict)

    def find_one(self,search_dict):
        result = self.find(search_dict)
        return result.next()

    def add_inner_index(self,index):
        def inner_index_maker():

            self.inner_index=index
            self.inner_index.collection=self.collection
        self.inner_index.fields_under=list(self.fields_under)
        self.inner_index.fields_under.append(self.field_name)

    def create(self,search_dict,collection):
        if self.created:
            self.index[search_dict[self.field_name]].find(search_dict)
        else:
            for element in collection.find({}):
                self.insert(element)
    def insert_element(self,element):
        pass

class DictIndex(Index):
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



class Storage(object):

    def __init__(self,name,index_list):

        self.collection=Config()['default_database'][name]
        self.cache_enabled=Config()['cache_enabled']
        self.idx=None

        self.elements=[]



        for index in index_list:
        self.collection.create_index(index.field_name)
            if self.cache_enabled:
                if self.idx:
                    self.idx.add_inner_index(index)
                else
                    self.idx=index
                    self.idx.collection=self.collection

        self.find=self.collection.find
        self.find_one=self.collection.find_one
        self.insert_one=self.collection.insert_one
        self.insert_many=self.collection.insert_many
        self.delete_many=self.collection.delete_many
        self.count=self.collection.count

        # Create basic index
        if self.cache_enabled:
            self.find=self.idx.find
            self.find_one=self.idx.find_one
            self.insert_one=self.idx.insert_one
            self.insert_many=self.idx.insert_many

            self.count=self.idx.count
            slef.

    def commit(self):
        self.idx.commit()

    def to_ram(self):


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
