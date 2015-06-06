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

# src dst selec
sources_key='src'
destinations_key='dst'
selectivity_key='sel'

#ring
ring_key='r'
to_ring_total_key="to_ring_total"
in_ring_total_key="in_ring_total"

# surplus weight for cut-offs
sd_surplus=0

# dendryt pred succ
predecessor_key='x'
successor_key='y'



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