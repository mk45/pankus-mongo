#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.exporters.export_to_geojson import export

def export_line_conn():
    export('line_conn')

if __name__ == "__main__":
    export('line_conn')
