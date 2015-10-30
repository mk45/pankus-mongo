#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.line_conn import line_conn as line_conn
from pankus.helpers.pbar import Pbar
from pankus.storages.stress import stress
from pankus.helpers.ram_collection import RamCollection


def remove_stress_info():

    pbar = Pbar('removing stress info: ',line_conn.count())
    stress.delete_many({})

    ram_line_conn=RamCollection(line_conn)

    for edge in ram_line_conn.find():
        pbar.plus_one()
        if stress_key in edge:
            del(edge[stress_key])
        if junction_key in edge:
            del(edge[junction_key])
        if interlace_key in edge:
            del(edge[interlace_key])

    line_conn.delete_many({})
    line_conn.insert_many(ram_line_conn.find())
    pbar.finish()


if __name__ == "__main__":
    remove_stress_info()
