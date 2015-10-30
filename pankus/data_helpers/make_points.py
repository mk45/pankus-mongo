#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.line_conn import line_conn
from pankus.storages.point import point
from pankus.helpers.pbar import Pbar

def make_points():
    point_id = 0

    point_id_index_by_xy = {}

    new_line_conn = []

    pbar=Pbar('extracting points',line_conn.count())

    for line in line_conn.find():
        pbar.plus_one()
        start_xy = tuple(line[linestring_key][0])
        end_xy = tuple(line[linestring_key][-1])

        if start_xy not in point_id_index_by_xy:
            point_id_index_by_xy[start_xy] = point_id
            point_id += 1
        start = point_id_index_by_xy[start_xy]

        if end_xy not in point_id_index_by_xy:
            point_id_index_by_xy[end_xy] = point_id
            point_id += 1
        end = point_id_index_by_xy[end_xy]

        line[start_key] = start
        line[end_key] = end
        new_line_conn.append(line)

    line_conn.delete_many({})
    line_conn.insert_many(new_line_conn)

    point.delete_many({})
    point.insert_many([{id_key: point_id_index_by_xy[xy], point_key: xy}
                          for xy in point_id_index_by_xy])
    pbar.finish()

if __name__ == "__main__":
    make_points()
