#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.line_conn import line_conn as line_conn
from pankus.helpers.pbar import Pbar
from pankus.storages.motion_exchange_withdrawal_excess import motion_exchange_withdrawal_excess
from pankus.defaults.config import \
    stress_key,start_key,end_key,junction_key,interlace_key
from pankus.helpers.ram_collection import RamCollection


def remove_stress_info():

    pbar = Pbar('removing stress info: ',line_conn.count())
    motion_exchange_withdrawal_excess.delete_many({})
    pbar.finish()


if __name__ == "__main__":
    remove_stress_info()
