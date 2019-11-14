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

top_left_lon = -83.082279
top_left_lat = 42.327830

nrows = 13
ncols = 16

rotation = 23


cell_size = 30
crs_epsg = '26917'

col_margin_left=7 # columns to add to left of interactive grid to create full grid
row_margin_top=15 # rows to add to top of interactive grid to create full grid
full_cell_width=62 # total num columns in full grid
full_cell_height=54 # total num rows in full grid


# First create the interactive grid
corktown_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

# then extend it to create the full grid
corktown_grid.extend_int_grid_to_full(col_margin_left,  row_margin_top, full_cell_width, full_cell_height)
corktown_grid.plot()

land_use=json.load(open('examples/land_use_data/corktown_landuse.geojson'))
lu_property='ZONING'
corktown_grid.get_land_uses(land_use, lu_property, include_interactive_cells=True)

grid_geo=corktown_grid.get_grid_geojson(add_properties={'height': [10]*len(
        corktown_grid.grid_coords_ll)})

# post to cityIO
output_url='https://cityio.media.mit.edu/api/table/update/corktown/'
r = requests.post(output_url+'meta_grid', data = json.dumps(grid_geo))
print('Meta_grid:')
print(r)
r = requests.post(output_url+'interactive_grid_mapping', 
                  data = json.dumps(corktown_grid.int_to_meta_map))
print('Grid Mapping:')
print(r)

