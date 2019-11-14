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
# Fully interactive Grid
# =============================================================================


top_left_lon = 10.006775
top_left_lat = 53.537894

nrows = 44
ncols = 78

rotation = 145.5


cell_size = 16
crs_epsg = '31468'

col_margin_left=0 # columns to add to left of interactive grid to create full grid
row_margin_top=0 # rows to add to top of interactive grid to create full grid
full_cell_width=ncols # total num columns in full grid
full_cell_height=nrows # total num rows in full grid


# First create the interactive grid
grasbrook_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

# then extend by zero cells to create the full grid
grasbrook_grid.extend_int_grid_to_full(col_margin_left,  row_margin_top, full_cell_width, full_cell_height)
grasbrook_grid.plot()

grid_geo=grasbrook_grid.get_grid_geojson(add_properties={})

# save JSON files
# json.dump(grasbrook_grid.int_to_meta_map, open(MAP_FILE_PATH, 'w'))
# json.dump(grid_geo, open(GEO_FILE_PATH, 'w'))


# =============================================================================
# Interactive Area by Land Use values (all interactive except if LU==None)
# =============================================================================

grasbrook_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

land_use=json.load(open('examples/land_use_data/grasbrook_osm_landuse.geojson'))
lu_property='fclass'
# Using a hack for now- eventually to be made a class method
grasbrook_grid.properties={'interactive': [False for i in range(len(grasbrook_grid.grid_coords_ll))]}
grasbrook_grid.get_land_uses(land_use, lu_property,include_interactive_cells=True)

interactive=[]
interactive_id=[]
int_to_meta_map={}

int_id=0
for meta_ind, lu in enumerate(grasbrook_grid.properties['land_use']):
    if lu=='None':
        interactive.append(False)
        interactive_id.append(None)
    else:
        interactive.append(True)
        interactive_id.append(int_id)
        int_to_meta_map[int_id]=meta_ind
        int_id+=1

grasbrook_grid.properties['interactive']=interactive
grasbrook_grid.properties['interactive_id']=interactive_id
grasbrook_grid.int_to_meta_map=int_to_meta_map

################### Hack until we have LU mapping ################

mapped_lu=[]
for lu in grasbrook_grid.properties['land_use']:
    if lu=='industrial':
        mapped_lu.append('M1')
    else:
        mapped_lu.append('None')
grasbrook_grid.properties['land_use']=mapped_lu

#################################################################

grid_geo=grasbrook_grid.get_grid_geojson(add_properties={})






