#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.exporters.export_to_geojson import export

def export_sd_point():
    export('sd_point')

if __name__ == "__main__":
    export('sd_point')
