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

top_left_lon =  -83.083773
top_left_lat = 42.330525

nrows = 16
ncols = 20

rotation = 23


cell_size = 15
crs_epsg = '26917'

col_margin_left=10 # columns to add to left of interactive grid to create full grid
row_margin_top=10 # rows to add to top of interactive grid to create full grid
full_cell_width=60 # total num columns in full grid
full_cell_height=30 # total num rows in full grid


# First create the interactive grid
corktown_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

# then extend it to create the full grid
corktown_grid.extend_int_grid_to_full(col_margin_left,  row_margin_top, full_cell_width, full_cell_height)
corktown_grid.plot()

land_use=json.load(open('examples/land_use_data/corktown_landuse.geojson'))
lu_property='ZONING'
corktown_grid.get_land_uses(land_use, lu_property)

grid_geo=corktown_grid.get_grid_geojson(add_properties={'height': [10]*len(
        corktown_grid.grid_coords_ll)})

# post to cityIO
output_url='https://cityio.media.mit.edu/api/table/update/corktown/meta_grid'
r = requests.post(output_url, data = json.dumps(grid_geo))
print(r)

