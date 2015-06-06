#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='pankus',
    version='0.1',
    packages=[
        'pankus',
        'pankus.storages',
        'pankus.database',
        'pankus.defaults',
        'pankus.importers',
        'pankus.intopp',
        'pankus.paths',
        'pankus.helpers',
        'pankus.data_helpers',
        'pankus.stress',
    ],
    url='http://github.com/mk45/pankus',
    license='(c) Politechnika Wroclawska',
    author='Maciej Kamiński',
    author_email='maciej.kaminski@pwr.edu.pl',
    description='Spatial planning software'

)
