#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


default_config={
'default_database':'pankus',
#
# if cache? RAM or db oriented execution
'cache_enable':True,

# what must be covered
# crs
'crs_key':'crs',
# point linestring
'point_key':'point',
'linestring_key':'linestring',
# weight throughput
'weight_key':'weight',
'throughput_key':'throughput',
# s e id
'start_key':'s',
'end_key':'e',
'id_key':'id',
# sd_s sd_e sd_id
'sd_start_key':'sd_s',
'sd_end_key':'sd_e',
'sd_id_key':'sd_id',
# net sd_points
# importers adds an extension
'net_filename':'net',
'sd_filename':'sd',
# net_out sd_points_out
'net_out_filename':'net_out',
'sd_out_filename':'sd_out',
# stress
'stress_key':'strs',
'motion_quantity_key':'q',
'junction_key':'junc',
'interlace_key':'intl',
'weight_increase_function': '1+x**6', # must be rather short decrease  function

#determinants
'interlace_determinant_key':'intl_det',
'junction_determinant_key':'junc_det',

#junction
'ordered_predecessors_key':'ordered_predecessors',
'ordered_successors_key':'ordered_successors',

#ordered junction/interlace info
'ordered_junction_info_key':"ordered_junc",
'ordered_interlace_info_key':"ordered_intl",


# src dst selec
'sources_key':'src',
'destinations_key':'dst',
'selectivity_key':'sel',

#ring
'ring_key':'r',
'to_ring_total_key':"to_ring_total",
'in_ring_total_key':"in_ring_total",
'points_in_ring_key':"points_in_ring",
# surplus weight for cut-offs

'sd_surplus':100000,
'blocking_weight':100000,

# dendryt pred succ
'successor_key':'x',
'predecessor_key':'y',

#path option
'path_key':'path',
'delta_key':'d',

#vector repair constants
'warn_search_size':1,
'repair_size':2**-6,

#system warning memory
'reserved_free_memory': 32000000L,

# collection names
'config':'config',
'line_conn':"line_conn",
'connection':"connection",
'crs':"crs",
'dendryt':"dendryt",
'featured_point':"featured_point",
'point':"point",
'sd_point':"sd_point",
'stress':"stress",
'src_dst':"src_dst",
'ring':"ring",
'ring_total':"ring_total",
'motion_exchange':"motion_exchange",
'turn_info':"turn_info",
'stress_matrix':"stress_matrix",
'path':"path",
'sd_to_ring_motion':"sd_to_ring_motion",
'voting_table':"votes",

# analisys
'to_point_motion_key':"to_point_motion",
'to_ring_motion_key':"to_ring_motion",
'satisfied_destinations_part_key':"satisfied_destinations"

}