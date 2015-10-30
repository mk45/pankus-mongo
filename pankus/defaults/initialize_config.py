#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.config import config
from pankus.defaults.default_config import default_config

def initialize_config(**kwargs):
    for keyword in default_config:
        if keyword not in kwargs:
            kwargs[keyword]=default_config[keyword]
        globals()[keyword]=kwargs[keyword]

    config.delete_many({})
    config.insert_one(kwargs)

