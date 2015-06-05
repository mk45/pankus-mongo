#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

# from pankus.storage.sd_point import sd_point
import json
from pankus.storage.sd_point import sd_point
from pankus.storage.crs import crs
from pankus.defaults.config import \
    sd_id_key,sources_key,destinations_key,point_key,sd_filename,crs_key
from pankus.helpers.pbar import Pbar


def import_sd_points():
    with open(sd_filename+'.geojson') as f:
        geo_data = json.load(f)
        assert geo_data['type'] == 'FeatureCollection'
        pbar = Pbar('importing sd: ',len(geo_data['features']))
        assert crs.count() == 0 or crs.find_one()[crs_key]==geo_data["crs"]

        sd_point.delete_many({})

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
            sd_point.insert_one(record)
        pbar.finish()

if __name__ == "__main__":
    import_sd_points()
