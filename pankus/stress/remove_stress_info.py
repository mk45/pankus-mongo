#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.line_conn import line_conn as line_conn
from pankus.helpers.pbar import Pbar
from pankus.storages.stress import stress
from pankus.defaults.config import \
    stress_key,start_key,end_key,junction_key,interlace_key


def remove_stress_info():

    pbar = Pbar('removing stressinfo: ',line_conn.count())
    stress.delete_many({})

    for edge in line_conn.find():
        pbar.plus_one()
        line_conn.update_one({
            start_key: edge[start_key],
            end_key: edge[end_key]
        },{
            "$unset": {
                stress_key: "",
                junction_key: "",
                interlace_key: ""}
        })
    pbar.finish()


if __name__ == "__main__":
    remove_stress_info()
