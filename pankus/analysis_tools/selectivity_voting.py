#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'

from math import exp,sqrt,log,copysign,pow
from pankus.storages.src_dst import src_dst
from pankus.storages.sd_to_ring_motion import sd_to_ring_motion
from pankus.storages.voting import voting
from pankus.helpers.ram_collection import RamCollection
from pankus.helpers.pbar import Pbar

def selectivity_voting(iteration):
    #src_total = sum([sd[sources_key] for sd in src_dst.find()])
    #dst_total = sum([sd[destinations_key] for sd in src_dst.find()])

    def normalize_avg(l,m,t):
        return ((l-1)/(m-1))*(t-1)+1

    pbar = Pbar('make voting: ',src_dst.count())
    votes=RamCollection(voting)

    new_src_dst=[]
    max_vote=max(a["ms"] for a in votes.find())
    min_vote=min(a["ms"] for a in votes.find())
    print "mv:",min_vote
    print "lv:",max_vote
    for point in src_dst.find():
        pbar.plus_one()

        weighted_sum=sum([pow(a[satisfied_destinations_part_key],a["near"])*a["px"]*abs(a["ms"])*a["near"]
                          for a in votes.find({sd_end_key:point[sd_id_key]})])
        weights_sum=sum([a["px"]*abs(a["ms"])*a["near"]
                          for a in votes.find({sd_end_key:point[sd_id_key]})])
        if weights_sum==0:
            sum_votes=1
        else:
            sum_votes=weighted_sum/weights_sum

        if sum_votes>1:
            multiplier=1/(sum_votes**1)
        elif sum_votes==1:
            multiplier=1
        else:
            multiplier=1/(sum_votes**1)

        print point[sd_id_key],sum_votes,multiplier

        new_selectivity=point[selectivity_key]*multiplier
        if multiplier>1 and point[selectivity_key]>200:
            new_selectivity=point[selectivity_key]

        new_src_dst.append({
            sd_id_key:point[sd_id_key],

            sources_key:point[sources_key],
            destinations_key:point[destinations_key],
            selectivity_key:new_selectivity
        })

    src_dst.delete_many({})
    src_dst.insert_many(new_src_dst)
    pbar.finish()
