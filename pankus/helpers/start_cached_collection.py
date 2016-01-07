#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.point import point

class StartCachedCollection(object):
    """
    This collection is used for speed up search by reading blocks with common start
    and search them by end
    this is useful when you want fast access to data in memory and still want to
    rotate scope
    """
    def __init__(self,basecoll,start_key,end_key):
        """

        :param basecoll: base collection
        :param start_key: key that changes slowly / not often
        :param end_key: key that is some how random but in

        questioning elements comes from point size
        """
        self.basecoll=basecoll
        self.cached_d=[]
        self.cached_d_node=None
        self.sk=start_key
        self.ek=end_key

    
    
    def find(self,search_opt):
        if len(search_opt)==2 and self.sk in search_opt and self.ek in search_opt:
            if self.cached_d_node!=search_opt[self.sk]:
                self.cached_d=[[] for i in xrange(point.count())]
                self.cached_d_node=search_opt[self.sk]
                
                for d in self.basecoll.find({self.sk:search_opt[self.sk]}):
                    while not len(self.cached_d)>d[self.ek]:
                        self.cached_d.append([])
                    self.cached_d[d[self.ek]].append(d)
            return self.cached_d[search_opt[self.ek]]
        else:
            raise ValueError()
        
    def find_one(self,search_opt):
        return  self.find(search_opt)[0]
        