#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from math import exp,sqrt,log,copysign,pow
from pankus.storages.src_dst import src_dst
from pankus.storages.votes import votes
from pankus.storages.sd_point import sd_point
from pankus.storages.src_dst import src_dst
from pankus.storages.ring import ring
from pankus.storages.ring_total import ring_total
from pankus.storages.motion_exchange import motion_exchange
from pankus.helpers.ram_collection import RamCollection
from pankus.helpers.pbar import Pbar
from pankus.defaults.config import sd_id_key,sd_end_key,\
    selectivity_key,sources_key,destinations_key,motion_quantity_key,\
    sd_start_key,satisfied_destinations_key,ring_key,in_ring_total_key,to_ring_total_key

####################################
# there exist assumption that normalisation
# after motion exchange has been performed
#
def selectivity_voting(aggression):

    pbar = Pbar('make new selectivity: ',src_dst.count()+sd_point.count())

    ram_sd_point=RamCollection(sd_point,[sd_id_key])
    ram_motion_exchange=RamCollection(motion_exchange,[sd_start_key,sd_end_key])
    ram_ring = RamCollection(ring,[sd_start_key,sd_end_key])
    ram_src_dst=RamCollection(src_dst,[sd_id_key])
    ram_ring_total=RamCollection(ring_total,[sd_id_key,ring_key])

    # votes {sd_id : [vote from one sd ,vote from other sd]

    # DESTINATIONS DUTY
    # Count motions to me
    # Vote with weight
    new_votes=[]
    # motion denotes start and end not voting
    for sd_end in ram_sd_point.find({}):
        pbar.plus_one()

        total_to_sd_motion=\
            sum([mx[motion_quantity_key] for mx in ram_motion_exchange.find({
                sd_end_key:sd_end[sd_id_key]
            })])
        for sd_start in ram_sd_point.find({}):
            in_ring= ram_ring.find_one({
                sd_start_key: sd_start[sd_id_key],
                sd_end_key: sd_end[sd_id_key]
            })[ring_key]

            motion=ram_motion_exchange.find_one({
                sd_start_key:sd_start[sd_id_key],
                sd_end_key:sd_end[sd_id_key]
            })[motion_quantity_key]

            in_ring_total=ram_ring_total.find_one({
                sd_id_key: sd_start[sd_id_key],
                ring_key: in_ring
            })[in_ring_total_key]

            to_ring_total=ram_ring_total.find_one({
                sd_id_key: sd_start[sd_id_key],
                ring_key: in_ring
            })[to_ring_total_key]


            new_votes.append({
                sd_start_key: sd_start[sd_id_key],
                sd_end_key: sd_end[sd_id_key],
                satisfied_destinations_key: total_to_sd_motion,
                destinations_key: sd_end[destinations_key],
                motion_quantity_key:motion,
                in_ring_total_key: in_ring_total,
                to_ring_total_key: to_ring_total,
            })
    votes.delete_many({})
    votes.insert_many(new_votes)

    # SOURCES DUTY
    # find magic distance
    # Count Votes in magic distance weighted
    ram_votes=RamCollection(votes,[sd_start_key,sd_end_key])

    new_src_dst=[]
    for voted in ram_src_dst.find():
        pbar.plus_one()

        nominator=0
        denominator=0
        for voting in ram_src_dst.find():

            vote=ram_votes.find_one({
                sd_start_key:voted[sd_id_key],
                sd_end_key:voting[sd_id_key]
            })

            destinations = vote[destinations_key]
            motion = vote[motion_quantity_key]
            in_ring_total = vote[in_ring_total_key]
            to_ring_total=vote[to_ring_total_key]
            total_to_sd_motion=vote[satisfied_destinations_key]
            selectivity=voted[selectivity_key]

            if in_ring_total!=0:
                change_scaling_factor=(
                        (to_ring_total+in_ring_total)*exp(-(to_ring_total+in_ring_total)*selectivity/1000000)-\
                        (to_ring_total)*exp(-to_ring_total*selectivity/1000000)
                    )/in_ring_total
            else:
                change_scaling_factor=0

            #produce weighted sum
            nominator+=(total_to_sd_motion-destinations)*change_scaling_factor*motion
            denominator+=abs(change_scaling_factor*motion)


        if denominator!=0:
            weighted = nominator/denominator
        else:
            weighted =0

        multiplier = (destinations-weighted)/destinations
        print weighted,multiplier
        new_selectivity=voted[selectivity_key]
        if multiplier >0.5 and \
                multiplier <2 and \
                voted[selectivity_key]<200 and \
                voted[selectivity_key]>0.01:
            new_selectivity=voted[selectivity_key]*(multiplier)
        elif multiplier>2 and voted[selectivity_key]<200:
            new_selectivity=voted[selectivity_key]*2
        elif multiplier<0.5 and voted[selectivity_key]>0.1:
            new_selectivity=voted[selectivity_key]/2

        new_src_dst.append({
            sd_id_key:voted[sd_id_key],
            sources_key:voted[sources_key],
            destinations_key:voted[destinations_key],
            selectivity_key: new_selectivity
        })

    src_dst.delete_many({})
    src_dst.insert_many(new_src_dst)
    pbar.finish()
