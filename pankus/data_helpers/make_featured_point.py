#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.sd_point import sd_point
from pankus.storages.featured_point import featured_point
from pankus.storages.point import point
from pankus.helpers.pbar import Pbar

def make_featured_points():
    pbar = Pbar('featured point: ',sd_point.count())
    new_featured_point=[]
    for sd_p in sd_point.find():
        pbar.plus_one()
        p = point.find_one({point_key: sd_p[point_key]})
        assert p
        new_featured_point.append({
            point_key: sd_p[point_key],
            sd_id_key: sd_p[sd_id_key],
            id_key: p[id_key]
        })
    featured_point.delete_many({})
    featured_point.insert_many(new_featured_point)
    pbar.finish()

if __name__ == "__main__":
    make_featured_points()