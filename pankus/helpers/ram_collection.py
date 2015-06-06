#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


class RamCollection(object):
    """
    Reads content of collection into memory.
    Makes some indexes for data access.
    """

    def __insert_element(self, element):
        self.elements.append(element)
        for idx_field in self.index_dict:
            assert idx_field in element
            assert type(element[idx_field]) == int

            while len(self.index_dict[idx_field]) <= element[idx_field]:
                self.index_dict[idx_field].append([])
            self.index_dict[idx_field][element[idx_field]].append(element)

    def __init__(self, base_collection, indexes = None):
        if not indexes:
            indexes=base_collection.indexes
        assert len(indexes) <= 2
        self.base_collection = base_collection
        self.changed = False
        self.elements = []
        self.index_dict = {}

        for k in indexes:
            self.index_dict[k] = []

        for element in base_collection.find():
            self.__insert_element(element)

    def find(self, search_opt={}):
        if len(search_opt) == 1:
            k, v = search_opt.items()[0]
            assert k in self.index_dict
            return self.index_dict[k][v]
        elif len(search_opt) == 2:
            k1, v1 = search_opt.items()[0]
            assert k1 in self.index_dict
            k2, v2 = search_opt.items()[1]
            assert k2 in self.index_dict
            return [element for element in self.index_dict[k1][v1]
                    if element[k2] == v2]
        elif len(search_opt) == 0:
            return self.elements
        else:
            raise ValueError()

    def find_one(self, search_opt):
        return self.find(search_opt)[0]

    def count(self):
        return len(self.elements)

    def update_one(self, search_opt, update_opt, **kwargs):
        self.base_collection.update_one(search_opt, update_opt, **kwargs)

    def update_many(self, search_opt, update_opt, **kwargs):
        self.base_collection.update_many(search_opt, update_opt, **kwargs)

    def finalize(self):
        pass
