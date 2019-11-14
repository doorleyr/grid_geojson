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
# Simple Grid
# =============================================================================


top_left_lon = 10.01129157249875
top_left_lat = 53.53380541749196

nrows = 10
ncols = 10

rotation = 145.5


cell_size = 16
crs_epsg = '31468'

properties = {
    'id': [i for i in range(nrows*ncols)],
    'usage': [0 for i in range(nrows*ncols)],
    'height': [-100 for i in range(nrows*ncols)],
    'pop_density': [2 for i in range(nrows*ncols)]}
crs_epsg = '31468'

grasbrook_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)
grasbrook_grid.plot()

grid_geo = grasbrook_grid.get_grid_geojson(properties)
# =============================================================================
# Composite Grid
# =============================================================================

top_left_lon = 10.01129157249875
top_left_lat = 53.53380541749196

nrows = 10
ncols = 10

rotation = 145.5


cell_size = 16
crs_epsg = '31468'

col_margin_left=34 # columns to add to left of interactive grid to create full grid
row_margin_top=13 # rows to add to top of interactive grid to create full grid
full_cell_width=78 # total num columns in full grid
full_cell_height=44 # total num rows in full grid


# First create the interactive grid
grasbrook_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

# then extend it to create the full grid
grasbrook_grid.extend_int_grid_to_full(col_margin_left,  row_margin_top, full_cell_width, full_cell_height)
grasbrook_grid.plot()

land_use=json.load(open('examples/land_use_data/grasbrook_osm_landuse.geojson'))
lu_property='fclass'
grasbrook_grid.get_land_uses(land_use, lu_property, 
                      include_interactive_cells=True)

################### Hack until we have LU mapping ################

mapped_lu=[]
for lu in grasbrook_grid.properties['land_use']:
    if lu=='industrial':
        mapped_lu.append('M1')
    else:
        mapped_lu.append('None')
grasbrook_grid.properties['land_use']=mapped_lu

#################################################################

grid_geo=grasbrook_grid.get_grid_geojson(add_properties={'height': [10]*len(grasbrook_grid.grid_coords_ll)})

# post to cityIO
output_url='https://cityio.media.mit.edu/api/table/update/grasbrook/'
r = requests.post(output_url+'meta_grid', data = json.dumps(grid_geo))
print('Meta_grid:')
print(r)
r = requests.post(output_url+'interactive_grid_mapping', 
                  data = json.dumps(grasbrook_grid.int_to_meta_map))
print('Grid Mapping:')
print(r)

