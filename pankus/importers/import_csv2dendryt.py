#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'



import csv
from pankus.storages.dendryt import dendryt
from pankus.defaults.config import \
    start_key,end_key,weight_key,distances_filename
from pankus.helpers.pbar import Pbar


def import_csv2dendryt():
    with open(distances_filename+'.csv','rb') as f:
        new_dendryt=[]
        file_content=f.readlines()
        file_content_merged=''.join(file_content)
        pbar = Pbar('importing distances:',len(file_content))
        sniffer=csv.Sniffer()
        has_header=sniffer.has_header(file_content_merged)
        assert has_header
        dialect=sniffer.sniff(file_content_merged)
        csv_reader=csv.DictReader(file_content,dialect=dialect)
        for line_record in csv_reader:
            pbar.plus_one()
            assert start_key in line_record
            assert end_key in line_record
            assert weight_key in line_record
            new_dendryt.append(line_record)

        dendryt.delete_many({})
        dendryt.insert_many(new_dendryt)
        pbar.finish()

if __name__ == "__main__":
    import_csv2dendryt()
