#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


def weight_increase_function(load):
    """
    :param load: stress divided by throughput
    :return: weight increase factor

    how does weight increases on stress load

    """

    return 1+1*load**6
    #return 0.0098+0.0256*(load)**6
