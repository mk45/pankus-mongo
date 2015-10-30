#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.config import config
from pankus.defaults.default_config import default_config

def get_config(name=None):
    cfg_line=config.find_one()
    if cfg_line and name in cfg_line:
        return cfg_line[name]
    else:
        return default_config[name]
