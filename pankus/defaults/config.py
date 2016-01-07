#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

default_database = 'pankus'


#
# what must be covered
# crs
crs_key='crs'
# point linestring
point_key='point'
linestring_key='linestring'
# weight throughput
weight_key='weight'
throughput_key='throughput'
# s e id
start_key='s'
end_key='e'
id_key='id'
# sd_s sd_e sd_id
sd_start_key='sd_s'
sd_end_key='sd_e'
sd_id_key='sd_id'
# net sd_points
# importers adds an extension
net_filename='net'
sd_filename='sd'
# net_out sd_points_out
net_out_filename='net_out'
sd_out_filename='sd_out'
# stress
stress_key='strs'
motion_quantity_key='q'
junction_key='junc'
interlace_key='intl'

#determinants
interlace_determinant_key='intl_det'
junction_determinant_key='junc_det'

#junction
ordered_predecessors_key = 'ordered_predecessors'
ordered_successors_key = 'ordered_successors'

#ordered junction/interlace info
ordered_junction_info_key = "ordered_junc"
ordered_interlace_info_key = "ordered_intl"


# src dst selec
sources_key='src'
destinations_key='dst'
selectivity_key='sel'

#ring
ring_key='r'
points_in_ring_key='points_in_ring'
to_ring_total_key="to_ring_total"
in_ring_total_key="in_ring_total"

# surplus weight for cut-offs

sd_surplus=0
#sd_surplus=100000
blocking_weight=100000

# dendryt pred succ
successor_key='x'
predecessor_key='y'

#path option
path_key='path'
delta_key='d'

#vector repair constants
warn_search_size = 1
repair_size = 2**-6

# selectivity changes voting
votes_table_name='votes'
satisfied_destinations_key='sat_dst'

# collection names
line_conn_name="line_conn"
connection_name = "connection"
crs_name="crs"
dendryt_name="dendryt"
featured_point_name="featured_point"
point_name="point"
sd_point_name="sd_point"
stress_name="stress"
src_dst_name="src_dst"
ring_name="ring"
ring_total_name="ring_total"
motion_exchange_name="motion_exchange"
motion_exchange_withdrawal_excess_name="motion_exchange_we"
turn_info_name="turn_info"
stress_matrix_name="stress_matrix"
path_name= "path"