#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.storages.line_conn import line_conn
from pankus.storages.sd_point import sd_point
from pankus.helpers.pbar import Pbar


def repair():
    """
    Function repairs network. Binds junction points along with sd_points to grid.
    that snaps together scattered junctions
    :return:
    """
    #
    # rebind point in repair_size range to one single
    # point with coordinates 2**-n
    #

    # make indexed line
    # lines in ram and index them by terminating points
    ram_lines = list(line_conn.find())
    ram_line_list_index_by_xy = {}

    ram_sd_points = list(sd_point.find())
    sd_point_index_by_xy = {}

    # populate ram_lines index

    for ram_lines_element in ram_lines:
        first = tuple(ram_lines_element[linestring_key][0])
        last = tuple(ram_lines_element[linestring_key][-1])

        if first not in ram_line_list_index_by_xy:
            ram_line_list_index_by_xy[first] = [ram_lines_element]
        else:
            ram_line_list_index_by_xy[first].append(ram_lines_element)

        if last not in ram_line_list_index_by_xy:
            ram_line_list_index_by_xy[last] = [ram_lines_element]
        else:
            ram_line_list_index_by_xy[last].append(ram_lines_element)

    # populate sd_points index
    for sd in ram_sd_points:
        sd_xy=tuple(sd[point_key])
        if sd_xy in sd_point_index_by_xy:
            raise ValueError(
                "Multiple sd point in same location are FORBIDDEN" + str(sd_xy))
        sd_point_index_by_xy[sd_xy]=sd

    #repair points in each line
    pbar = Pbar("repairing network",len(ram_line_list_index_by_xy))

    for point_to_repair in ram_line_list_index_by_xy.keys():
        pbar.plus_one()
        # point could be deleted somewhere so for sure lets check
        if point_to_repair in ram_line_list_index_by_xy:
            p_v = complex(*point_to_repair)
            # find any other points near by
            points_to_rebind = [xy
                                for xy in ram_line_list_index_by_xy
                                if abs(p_v - complex(*xy)) < repair_size
                                ]
            # create new point for rebind points
            new_x = int(point_to_repair[0] / repair_size) * repair_size
            new_y = int(point_to_repair[1] / repair_size) * repair_size
            new_xy = (new_x, new_y)

            # rebind each point to rebind
            # set new in each linestring
            for xy_to_rebind in points_to_rebind:
                if new_xy == xy_to_rebind or \
                                xy_to_rebind not in ram_line_list_index_by_xy:
                    continue
                if new_xy not in ram_line_list_index_by_xy:
                    ram_line_list_index_by_xy[new_xy] = []

                for ram_lines_element in ram_line_list_index_by_xy[xy_to_rebind]:
                    if tuple(ram_lines_element[linestring_key][0]) == xy_to_rebind:
                        ram_lines_element[0] = list(new_xy)
                    elif tuple(ram_lines_element[linestring_key][-1]) == xy_to_rebind:
                        ram_lines_element[-1] = list(new_xy)
                    else:
                        pass

                    ram_line_list_index_by_xy[new_xy] = ram_lines_element
                del (ram_line_list_index_by_xy[points_to_rebind])

            sd_points_to_rebind = [xy
                                for xy in sd_point_index_by_xy
                                if abs(p_v-complex(*xy))<repair_size
                                   ]
            assert len(sd_points_to_rebind)<2
            if len(sd_points_to_rebind)==1:
                sd_xy=sd_points_to_rebind[0]
                sd_point_index_by_xy[new_xy]=sd_point_index_by_xy[sd_xy]
                sd_point_index_by_xy[new_xy][point_key]=list(new_xy)
                del(sd_point_index_by_xy[sd_xy])

    # We use only [x,y] coordinates not [x,y,z]
    assert all([
                   all([
                           len(point_list) == 2
                           for point_list in line[linestring_key]
                           ]) for line in ram_lines
                   ])
    line_conn.delete_many({})
    line_conn.insert_many(ram_lines)

    sd_point.delete_many({})
    sd_point.insert_many(ram_sd_points)

    pbar.finish()

if __name__ == "__main__":
    repair()
