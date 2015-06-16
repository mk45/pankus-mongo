#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

import argparse
import json
from pankus.storages.point import point
from pankus.storages.featured_point import featured_point
from pankus.storages.connection import connection
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    start_key, weight_key, end_key, blocking_weight, id_key
from pankus.defaults.config import sd_surplus
from pankus.helpers.ram_collection import RamCollection

def block_junctions(point_list):
    """ Function blocks junctions. Nothing can gets through

    :param point_list: list of points to block. As list of ids or list of coordinates pairs
    """
    assert type(point_list)==list

    # we want id here
    def to_point_id(p):
        if (type(p)==list or type(p)==tuple) and \
                        len(p)==2 and \
                        type(p[0])==float and \
                        type(p[1])==float :
            p=point.find_one({'p':list(p)})['id']
        assert type(p)==int
        return p
    point_list=map(to_point_id,point_list)

    pbar=Pbar('turnoff junction: ',featured_point.count())

    ram_connection=RamCollection(connection)
    featured_point_id_list=[p[id_key] for p in featured_point.find()]

    for p in point_list:
        assert p not in featured_point_id_list
        for conn in ram_connection.find({start_key:p}):
            conn[weight_key]=blocking_weight

        for conn in ram_connection.find({end_key:p}):
            conn[weight_key]=blocking_weight

    for sd_point in featured_point.find():
        pbar.plus_one()
        id_of_sd=sd_point[id_key]
        next_points=[e[end_key] for e in ram_connection.find({start_key:id_of_sd})]
        if set(next_points)<=set(point_list):

            for c in next_points:
                conn.update({start_key:id_of_sd,end_key:c},\
                    {'$set':{weight_key:0}})

                conn.update({end_key:id_of_sd,start_key:c},\
                    {'$set':{weight_key:0}})

    pbar.finish()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("points",help="geojson encoded list of ",type=str)
    args=parser.parse_args()

    turn_off_function(json.loads(args.points))
