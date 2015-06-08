#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.helpers.pbar import Pbar
from pankus.storages.sd_point import sd_point
from pankus.storages.src_dst import src_dst
from pankus.defaults.config import sd_id_key,sources_key,destinations_key
import argparse


def save_src_dst_to_sd_point(src_name, dst_name):
    """
    :param src_name: name for sources in sd_point collection
    :param dst_name: name for destinations in sd_point collection
    :return:

    """
    pbar = Pbar('saving : ',src_dst.count())
    for sd in src_dst.find():
        pbar.plus_one()

        sd_point.update_one({
            sd_id_key: sd[sd_id_key]
        }, {'$set': {
            src_name: sd[sources_key],
            dst_name: sd[destinations_key]
        }
        })
    pbar.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sd_names", nargs=2, type=str)
    args = parser.parse_args()
    save_src_dst_to_sd_point(args.sd_names[0], args.sd_names[1])
