#!/usr/bin/env python2
# -*- coding: utf-8 -*-
__author__ = 'Maciej Kamiński Politechnika Wrocławska'


from pankus.importers.geojson2line_conn import import_lines
from pankus.importers.geojson2sd_point import import_sd_points
from pankus.data_helpers.make_featured_point import make_featured_points
from pankus.data_helpers.make_connections import make_connections
from pankus.data_helpers.make_stress_determinants import make_stress_determinants
from pankus.data_helpers.make_junction_turn_info import make_junction_turn_info
from pankus.data_helpers.save_src_dst_to_sd_point import save_src_dst_to_sd_point
from pankus.data_helpers.save_stress_to_line_conn import save_stress_to_line_conn
from pankus.intopp.make_src_dst import make_src_dst
from pankus.intopp.make_weight_rings import make_weight_rings
from pankus.intopp.make_rings_total import make_rings_total
from pankus.intopp.make_motion_exchange import make_motion_exchange
from pankus.intopp.make_shift import make_shift
from pankus.intopp.normalize_to_original import normalize_to_original
from pankus.intopp.make_dst_shift import make_destinations_shift
from pankus.intopp.make_gen_shift import make_general_shift
from pankus.paths.make_dendryts import make_dendryts
from pankus.paths.make_kpaths import make_kpaths
from pankus.stress.remove_stress_info import remove_stress_info
from pankus.stress.make_stress_matrix import make_stress_matrix
from pankus.stress.stress_kpaths import stress_kpaths
from pankus.exporters.export_line_conn import export_line_conn
from pankus.exporters.export_sd_point import export_sd_point



#import from files
import_lines()
import_sd_points()

make_featured_points()
make_connections()
make_dendryts()
make_src_dst(45)
make_weight_rings(300)
make_rings_total()
make_motion_exchange()
normalize_to_original()
make_destinations_shift()
save_src_dst_to_sd_point('src1','dst1')
make_stress_matrix(0.07)
make_junction_turn_info()
remove_stress_info()
make_kpaths(3)
stress_kpaths()
make_connections()
save_stress_to_line_conn()
make_stress_determinants()
export_line_conn()
export_sd_point()
