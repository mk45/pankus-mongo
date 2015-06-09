#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.helpers.iterate_consecutive_elements \
    import iterate_consecutive_n_elements
from pankus.storages.stress import stress
from pankus.storages.stress_matrix import stress_matrix
from pankus.helpers.start_cached_collection import StartCachedCollection
from pankus.storages.featured_point import featured_point
from pankus.storages.path import path
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import \
    id_key, start_key, end_key, motion_quantity_key, sd_start_key, \
    sd_end_key, path_key, stress_key, junction_key, interlace_key


def stress_kpaths(reverse=False):
    pbar = Pbar('stressing: ', featured_point.count())

    for sd_start in featured_point.find(no_cursor_timeout=True):
        start = sd_start[id_key]
        pbar.plus_one()
        stress_storage = []
        ram_path = StartCachedCollection(path, start_key, end_key)
        for sd_end in featured_point.find(no_cursor_timeout=True):
            end = sd_end[id_key]
            if start == end:
                continue
            # print end
            quantity = stress_matrix.find_one({
                start_key: start,
                end_key: end
            })[motion_quantity_key]

            paths_list = list(ram_path.find({start_key: start, end_key: end}))

            for p in paths_list:
                path_to_stress = p[path_key]
                if reverse:
                    path_to_stress.reverse()
                # put_stress(path_to_stress, quantity / len(paths_list), stress)
                if len(path_to_stress) <= 1:
                    raise ValueError()
                if len(path_to_stress) >= 2:
                    sd_s = path_to_stress[0]
                    sd_e = path_to_stress[-1]
                    stress_storage.append({
                        start_key: path_to_stress[0],
                        end_key: path_to_stress[1],
                        sd_start_key: sd_s,
                        sd_end_key: sd_e,
                        stress_key: quantity
                    })
                    if len(path_to_stress) >= 3:
                        stress_storage.append({
                            start_key: path_to_stress[-2],
                            end_key: path_to_stress[-1],
                            sd_start_key: sd_s,
                            sd_end_key: sd_e,
                            stress_key: quantity})
                        stress_storage.append({
                            start_key: path_to_stress[0],
                            end_key: path_to_stress[1],
                            sd_start_key: sd_s,
                            sd_end_key: sd_e,
                            junction_key: {str(path_to_stress[2]): quantity}
                        })
                        if len(path_to_stress) >= 4:
                            for p, s, e, f in iterate_consecutive_n_elements(path_to_stress, 4):
                                stress_storage.append({
                                    start_key: s,
                                    end_key: e,
                                    sd_start_key: sd_s,
                                    sd_end_key: sd_e,
                                    stress_key: quantity,
                                    junction_key: {str(f): quantity},
                                    interlace_key: {str(p): {str(f): quantity}}
                                })
        stress.insert_many(stress_storage)

    pbar.finish()


if __name__ == "__main__":
    stress_kpaths(reverse=False)
