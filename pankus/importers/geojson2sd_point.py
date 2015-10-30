#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


import json
from pankus.storages.sd_point import sd_point
from pankus.storages.crs import crs
from pankus.helpers.pbar import Pbar


def import_sd_points():
    with open(sd_filename+'.geojson') as f:
        geo_data = json.load(f)
        assert geo_data['type'] == 'FeatureCollection'
        pbar = Pbar('importing sd: ',len(geo_data['features']))
        assert crs.count() == 0 or crs.find_one()[crs_key]==geo_data["crs"]
        new_sd_point=[]
        for feature in geo_data['features']:
            pbar.plus_one()
            assert feature['type'] == 'Feature'
            assert feature['geometry']['type'] == 'Point'

            sd_p = feature['geometry']['coordinates']

            # build rcord
            assert sd_id_key in feature['properties']
            assert sources_key in feature['properties']
            assert destinations_key in feature['properties']
            assert point_key not in feature['properties']
            record = feature['properties']
            record[point_key] = sd_p
            new_sd_point.append(record)

        sd_point.delete_many({})
        sd_point.insert_many(new_sd_point)
        pbar.finish()

if __name__ == "__main__":
    import_sd_points()
