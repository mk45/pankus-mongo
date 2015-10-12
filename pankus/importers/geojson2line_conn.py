#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import json
from pankus.storages.line_conn import line_conn
from pankus.storages.crs import crs
from pankus.defaults.config import \
    crs_key,start_key,end_key,linestring_key,weight_key,net_filename
from pankus.helpers.pbar import Pbar


def import_lines():
    with open(net_filename+'.geojson') as f:
        geo_data = json.load(f)
        assert geo_data['type'] == 'FeatureCollection'

        crs.delete_many({})
        crs.insert_one({crs_key: geo_data["crs"]})

        pbar = Pbar('importing line:',len(geo_data['features']))

        new_line_conn=[]
        for feature in geo_data['features']:
            pbar.plus_one()
            assert feature['type'] == 'Feature'
            assert feature['geometry']['type'] == 'LineString'

            points = feature['geometry']['coordinates']

            # build record
            assert start_key not in feature['properties']
            assert end_key not in feature['properties']
            assert linestring_key not in feature['properties']
            assert weight_key in feature['properties']
            record = feature['properties']

            record[linestring_key] = points
            # r = line_conn.find_one({start_key: start_id, end_key: end_id})
            # if r:
            #     print r
            #     ipdb.set_trace()
            #     if r[weight_key] < record[weight_key]:
            #         print r
            #         ipdb.set_trace()
            #         continue
            #
            #     print [points[0], points[-1]]
            #
            #     raise ValueError(
            #         "Can't have multiple connection between points")
            new_line_conn.append(record)
        line_conn.delete_many({})
        line_conn.insert_many(new_line_conn)
        pbar.finish()

if __name__ == "__main__":
    import_lines()
