#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json

import ipdb

from pankus.storage.line_conn import line_conn
from pankus.storage.point import point
from pankus.storage.crs import crs
from pankus.defaults.config import \
    crs_key,point_key,id_key,start_key,end_key,linestring_key,weight_key,net_filename
from pankus.helpers.pbar import Pbar


def import_lines():
    with open(net_filename+'.geojson') as f:
        geo_data = json.load(f)
        assert geo_data['type'] == 'FeatureCollection'
        crs.delete_many({})
        crs.insert_one({crs_key: geo_data["crs"]})

        pbar = Pbar('importing line:',len(geo_data['features']))

        line_conn.delete_many({})
        point_id = 0

        for feature in geo_data['features']:
            pbar.plus_one()
            assert feature['type'] == 'Feature'
            assert feature['geometry']['type'] == 'LineString'

            points = feature['geometry']['coordinates']
            start = point.find_one({point_key: points[0]})
            if not start:
                point.insert_one({point_key: points[0], id_key: point_id})
                start_id = point_id
                point_id += 1
            else:
                start_id = start[id_key]

            end = point.find_one({point_key: points[-1]})
            if not end:
                point.insert_one({point_key: points[-1], id_key: point_id})
                end_id = point_id
                point_id += 1
            else:
                end_id = end[id_key]

            # build record
            assert start_key not in feature['properties']
            assert end_key not in feature['properties']
            assert linestring_key not in feature['properties']
            assert weight_key in feature['properties']
            record = feature['properties']
            record[start_key] = start_id
            record[end_key] = end_id
            record[linestring_key] = points
            r = line_conn.find_one({start_key: start_id, end_key: end_id})
            if r:
                print r
                ipdb.set_trace()
                if r[weight_key] < record[weight_key]:
                    print r
                    ipdb.set_trace()
                    continue

                print [points[0], points[-1]]

                raise ValueError(
                    "Can't have multiple connection between points")

            line_conn.insert_one(record)
        pbar.finish()

if __name__ == "__main__":
    import_lines()
