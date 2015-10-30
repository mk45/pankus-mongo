#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from pankus.defaults.get_config import get_config
get_config()

# #
# global default_database
# default_database=get_config('default_database')()
# global config_name
# config_name=get_config('config_name')()
# global crs_key
# crs_key=get_config('crs_key')()
# global point_key
# point_key=get_config('point_key')()
# global linestring_key
# linestring_key=get_config('linestring_key')()
# global weight_key
# weight_key=get_config('weight_key')()
# global throughput_key
# throughput_key=get_config('throughput_key')()
# global start_key
# start_key=get_config('start_key')()
# global end_key
# end_key=get_config('end_key')()
# global id_key
# id_key=get_config('id_key')()
# global sd_start_key
# sd_start_key=get_config('sd_start_key')()
# global sd_end_key
# sd_end_key=get_config('sd_end_key')()
# global sd_id_key
# sd_id_key=get_config('sd_id_key')()
# global net_filename
# net_filename=get_config('net_filename')()
# global sd_filename
# sd_filename=get_config('sd_filename')()
# global net_out_filename
# net_out_filename=get_config('net_out_filename')()
# global sd_out_filename
# sd_out_filename=get_config('sd_out_filename')()
# global stress_key
# stress_key=get_config('stress_key')()
# global motion_quantity_key
# motion_quantity_key=get_config('motion_quantity_key')()
# global junction_key
# junction_key=get_config('junction_key')()
# global interlace_key
# interlace_key=get_config('interlace_key')()
# global interlace_determinant_key
# interlace_determinant_key=get_config('interlace_determinant_key')()
# global junction_determinant_key
# junction_determinant_key=get_config('junction_determinant_key')()
# global ordered_predecessors_key
# ordered_predecessors_key=get_config('ordered_predecessors_key')()
# global ordered_successors_key
# ordered_successors_key=get_config('ordered_successors_key')()
# global ordered_junction_info_key
# ordered_junction_info_key=get_config('ordered_junction_info_key')()
# global ordered_interlace_info_key
# ordered_interlace_info_key=get_config('ordered_interlace_info_key')()
# global sources_key
# sources_key=get_config('sources_key')()
# global destinations_key
# destinations_key=get_config('destinations_key')()
# global selectivity_key
# selectivity_key=get_config('selectivity_key')()
# global ring_key
# ring_key=get_config('ring_key')()
# global to_ring_total_key
# to_ring_total_key=get_config('to_ring_total_key')()
# global in_ring_total_key
# in_ring_total_key=get_config('in_ring_total_key')()
# global points_in_ring_key
# points_in_ring_key=get_config('points_in_ring_key')()
# global sd_surplus
# sd_surplus=get_config('sd_surplus')()
# global blocking_weight
# blocking_weight=get_config('blocking_weight')()
# global successor_key
# successor_key=get_config('successor_key')()
# global predecessor_key
# predecessor_key=get_config('predecessor_key')()
# global path_key
# path_key=get_config('path_key')()
# global delta_key
# delta_key=get_config('delta_key')()
# global warn_search_size
# warn_search_size=get_config('warn_search_size')()
# global repair_size
# repair_size=get_config('repair_size')()
# global line_conn_name
# line_conn_name=get_config('line_conn_name')()
# global connection_name
# connection_name=get_config('connection_name')()
# global crs_name
# crs_name=get_config('crs_name')()
# global dendryt_name
# dendryt_name=get_config('dendryt_name')()
# global featured_point_name
# featured_point_name=get_config('featured_point_name')()
# global point_name
# point_name=get_config('point_name')()
# global sd_point_name
# sd_point_name=get_config('sd_point_name')()
# global stress_name
# stress_name=get_config('stress_name')()
# global src_dst_name
# src_dst_name=get_config('src_dst_name')()
# global ring_name
# ring_name=get_config('ring_name')()
# global ring_total_name
# ring_total_name=get_config('ring_total_name')()
# global motion_exchange_name
# motion_exchange_name=get_config('motion_exchange_name')()
# global turn_info_name
# turn_info_name=get_config('turn_info_name')()
# global stress_matrix_name
# stress_matrix_name=get_config('stress_matrix_name')()
# global path_name
# path_name=get_config('path_name')()
# global sd_to_ring_motion_name
# sd_to_ring_motion_name=get_config('sd_to_ring_motion_name')()
# global voting_table_name
# voting_table_name=get_config('voting_table_name')()
# global to_point_motion_key
# to_point_motion_key=get_config('to_point_motion_key')()
# global to_ring_motion_key
# to_ring_motion_key=get_config('to_ring_motion_key')()
# global satisfied_destinations_part_key
# satisfied_destinations_part_key=get_config('satisfied_destinations_part_key')()