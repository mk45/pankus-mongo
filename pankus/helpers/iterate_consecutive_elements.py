#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


def iterate_consecutive_n_elements(li,n):
    """

    :param li: list to iterate
    :param n: number of elements
    :return: yields consecutive elements in form 1,2,3 ; 2,3,4 ; 4,5,6 ....

    """
    if len(li)>=n:
        for i in xrange(len(li)-n+1):
            yield tuple(li[i:i+n])
            
