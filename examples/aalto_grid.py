#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:23:31 2019

@author: doorleyr
"""

import json
import os
import sys
import requests


file_dir = os.path.dirname('grid_geojson')
sys.path.append(file_dir)
from module.grid_geojson import *  # nopep8


# =============================================================================
# Composite Grid
# =============================================================================

top_left_lon = 24.8161471
top_left_lat =  60.18643753

nrows = 28
ncols = 28

rotation = 45


cell_size = 28
crs_epsg = '3047'

col_margin_left=0 # columns to add to left of interactive grid to create full grid
row_margin_top=0 # rows to add to top of interactive grid to create full grid
full_cell_width=28 # total num columns in full grid
full_cell_height=28 # total num rows in full grid


# First create the interactive grid
aalto_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

# then extend it to create the full grid
aalto_grid.extend_int_grid_to_full(col_margin_left,  row_margin_top, full_cell_width, full_cell_height)
aalto_grid.plot()


grid_geo=aalto_grid.get_grid_geojson(add_properties={
        'height': [10]*len(aalto_grid.grid_coords_ll),
        'color': [[255,255,255]]*len(
        aalto_grid.grid_coords_ll)})

# post to cityIO
output_url='https://cityio.media.mit.edu/api/table/update/aalto_02/'
r = requests.post(output_url+'meta_grid', data = json.dumps(grid_geo))
print('Meta_grid:')
print(r)

r = requests.post(output_url+'interactive_grid_mapping', 
                  data = json.dumps(aalto_grid.int_to_meta_map))
print('Grid Mapping:')
print(r)

r = requests.post(output_url+'meta_grid_header', 
                  data = json.dumps({'ncols': full_cell_width, 'nrows': full_cell_height}))
print('Meta Header:')
print(r)