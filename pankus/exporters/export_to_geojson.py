#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pankus.storages.sd_point import sd_point
from pankus.storages.line_conn import line_conn
from pankus.storages.crs import crs
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    linestring_key,point_key,crs_key,net_out_filename,sd_out_filename
import json


def export(export_type, prop_list=None):
    if export_type == "line_conn":
        geometry_name = "LineString"
        geometry_inner_name = linestring_key
        out_file = net_out_filename
        output_object = line_conn
    elif export_type == "sd_point":
        geometry_name = "Point"
        geometry_inner_name = point_key
        out_file = sd_out_filename
        output_object = sd_point
    else:
        raise ValueError("No other option")
    geo_data = {}
    geo_data['type'] = 'FeatureCollection'

    geo_data["crs"] = crs.find_one()[crs_key]

    pbar = Pbar('exporting: ',output_object.count())
    geo_data["features"] = []
    for element in output_object.find():

        pbar.update(pbar.currval + 1)

        geo_data['features'].append({})
        geo_data['features'][-1]['type'] = 'Feature'
        geo_data['features'][-1]['geometry'] = {}
        geo_data['features'][-1]['geometry']['type'] = geometry_name
        geo_data['features'][-1]['geometry']['coordinates'] = \
            element[geometry_inner_name]
        geo_data['features'][-1]['properties'] = {}
        if not prop_list:
            prop_list = element.keys()
            prop_list.remove(geometry_inner_name)
            prop_list.remove('_id')

        for key in prop_list:
            value = element[key]

            if type(value) == float:
                geo_data['features'][-1]['properties'][key] = round(value, 6)
            elif type(value) == int:
                geo_data['features'][-1]['properties'][key] = value
            elif value is None:
                geo_data['features'][-1]['properties'][key] = None
            elif type(value) == unicode:
                geo_data['features'][-1]['properties'][key] =\
                    value.encode('utf-8')
            else:
                geo_data['features'][-1]['properties'][key] = str(value)
    with open(out_file+'.geojson', 'w') as f:
        json.dump(geo_data, f, indent=4)
    pbar.finish()
