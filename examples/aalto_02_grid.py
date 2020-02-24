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

table_name='aalto_02'

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

tui_top_left_row_index=0
tui_top_left_col_index=0
tui_num_interactive_rows=28
tui_num_interactive_cols=28


aalto_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

aalto_grid.add_tui_interactive_cells(tui_top_left_row_index, tui_top_left_col_index,
                                  tui_num_interactive_rows, tui_num_interactive_cols)
aalto_grid.flip_tui_ids_y()

grid_geo=aalto_grid.get_grid_geojson(add_properties={}, include_global_properties=False)

json.dump(grid_geo, open('examples/results/aalto_02_geogrid.geojson', 'w'))

aalto_grid.plot()

# =============================================================================
# post to cityIO
# =============================================================================
output_url='https://cityio.media.mit.edu/api/table/update/{}'.format(table_name)
r = requests.post(output_url+'/GEOGRID', data = json.dumps(grid_geo))
print('Geogrid:')
print(r)

#r = requests.post(output_url+'/GEOGRIDDATA', data = json.dumps(geogriddata))
#print('Geogriddata:')
#print(r)