#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


collections_config={
    'connection':{
        'index':['start_key','end_key'],
        'cached':'full',
        'fields':[
            'start_key',
            'end_key',
            'weight_key'
        ],
        'description':"Graph representation of line_conn with weight infuenced by traffic",
    },
    'dendryt':{
        'index':['start_key','end_key'],
        'cached':'partial',
        'fields':[
            'start_key',
            'end_key',
            'predecessor_key',
            'successor_key',
            'weight_key'
        ],
        'description':"distances from featured points to every other"
    },
    'featured_point':{
        'index':['sd_id_key','id_key'],
        'cached':'full',
        'fields':[
            'id_key',
            'sd_id_key',
            'point_key',
        ],
        'description':"src-dst points as points in real network",
    },
    'line_conn':{
        'index':['start_key','end_key'],
        'cached':'full',
        'fields':[
            'start_key',
            'end_key',
            'weight_key',
            'throughput_key',
            'stress_key',
            'junction_key',
            'interlace_key'
        ],
        'description':"Input output layer of roads with additional information of traffic"
    },
    'motion_exchange':{
        'index':['sd_start_key','sd_end_key'],
        'cached':'full',
        'fields':[
            'sd_start_key',
            'sd_end_key',
            'motion_quantity_key'
        ],
        'description':"Motion exchange between source and destination points (output from intervening opportunities model)"
    },
    'path':{
        'index':['start_key','end_key'],
        'cached':'partial',
        'fields':[
            'start_key',
            'end_key',
            'weight_key',
            'path_key',
            'delta_key'
        ],
        'description':"Contains multiple paths between start and end"
    },
    'point':{
        'index':['id_key'],
        'cached':'full',
        'fields':[
            'id_key',
            'point_key'
        ],
        'description':"Points from network, without linestring middle-points"
    },
    'ring':{
        'index':['sd_start_key','sd_end_key','ring_key'],
        'cached':'full',
        'fields':[
            'sd_start_key',
            'sd_end_key',
            'ring_key'
        ],
        'description':"Stores information that end point lays in witch ring of start point"
    },
    'ring_total':{
        'index':['sd_id_key','ring_key'],
        'cached':'full',
        'fields':[
            'sd_id_key',
            'ring_key',
            'in_ring_total_key',
            'to_ring_total_key',
            'points_in_ring_key'
        ],
        'description':"Stores information of points rings properties"
    },
    'sd_point':{
        'index':['sd_id_key','point_key'],
        'cached':'full',
        'fields':[
            'sd_id_key',
            'point_key',
            'sources_key',
            'destinations_key',
            'selectivity_key'
        ],
        'description':"Input output layer of sources/destinations with base information (selectivity not mandatory)"
    },
    #'sd_to_ring_motion':{
    #}
    'src_dst':{
        'index':['sd_id_key'],
        'cached':'full',
        'fields':[
            'sd_id_key',
            'sources_key',
            'destinations_key',
            'selectivity_key', #in parts per million
        ],
        'description':"Base collection for running intervening opportunities model, stores sources and destinations info"
    },
    'stress':{
        'index':['start_key','end_key','sd_start_key','sd_end_key'],
        'cached':'partial',
        'fields':[
            'start_key',
            'end_key',
            'sd_start_key',
            'sd_end_key',
            'stress_key',
            'junction_key',
            'interlace_key',

        ],
        'description':"Contains traffic on each edge split by source to destinations witch generates them"

    },
    'stress_matrix':{
        'index':['start_key','end_key'],
        'cached':'full',
        'fields':[
            'start_key',
            'end_key',
            'motion_quantity_key'
        ],
        'description':"Contains traffic exchange between points in network (amount put on network)"
    },
    'turn_info':{
        'index':['start_key','end_key'],
        'cached':'full',
        'fields':[
            'start_key',
            'end_key',
            'ordered_predecessors_key',
            'ordered_successors_key'
        ],
        'description':"Contains order of attachment other roads to road"
    }
}
