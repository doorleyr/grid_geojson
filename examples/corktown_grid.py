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

table_name='corktown'

# =============================================================================
# Composite Grid
# =============================================================================

top_left_lon =  -83.090119
top_left_lat = 42.336341

nrows = 46
ncols = 40

rotation = 23


cell_size = 50
crs_epsg = '26917'

tui_top_left_row_index=20
tui_top_left_col_index=10
tui_num_interactive_rows=0
tui_num_interactive_cols=0


corktown_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

corktown_grid.add_tui_interactive_cells(tui_top_left_row_index, tui_top_left_col_index,
                                  tui_num_interactive_rows, tui_num_interactive_cols)
# =============================================================================
# Set the web interactive region
# =============================================================================
interactive_region=json.load(open('examples/interactve_regions/corktown_interactive_area.geojson'))
corktown_grid.set_web_interactive_region(interactive_region)

land_use=json.load(open('examples/land_use_data/zoning_corktown.geojson'))
lu_property='ZONING_REV'
corktown_grid.get_land_uses(land_use, lu_property)

grid_geo=corktown_grid.get_grid_geojson(add_properties={})

# =============================================================================
#  Add types for web-based editing to header
# =============================================================================
types=json.load(open('examples/corktown_types.json'))
grid_geo['properties']['types']=types

# =============================================================================
# # INITIALISE GEOGRIDDATA
# =============================================================================
geogriddata=[{"color": [
                  0,
                  0,
                  0,
                  0
                ],
                "height": 0,
                "id": i,
                "interactive": grid_geo['features'][i]['properties']['interactive'],
                "land_use": grid_geo['features'][i]['properties']['land_use'],
                "name": "empty",
                "tui_id": None
              } for i in range(len(grid_geo['features']))]

# =============================================================================
# post to cityIO
# =============================================================================
output_url='https://cityio.media.mit.edu/api/table/update/{}'.format(table_name)
r = requests.post(output_url+'/GEOGRID', data = json.dumps(grid_geo))
print('Geogrid:')
print(r)

json.dump(grid_geo, open('examples/results/corktown_geogrid.geojson', 'w'))

corktown_grid.plot()

r = requests.post(output_url+'/GEOGRIDDATA', data = json.dumps(geogriddata))
print('Geogriddata:')
print(r)