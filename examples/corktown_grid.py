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
tui_num_interactive_rows=10
tui_num_interactive_cols=10


corktown_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

corktown_grid.add_tui_interactive_cells(tui_top_left_row_index, tui_top_left_col_index,
                                  tui_num_interactive_rows, tui_num_interactive_cols)


land_use=json.load(open('examples/land_use_data/zoning_corktown.geojson'))
lu_property='ZONING_REV'
corktown_grid.get_land_uses(land_use, lu_property)

grid_geo=corktown_grid.get_grid_geojson(add_properties={})

# Add the land use mapping to the properties of the geojson
grid_geo['properties']['LANDUSEINPUT']={
  "1": "Residential",
  "2": "Office",
  "3": "Retail",
  "4": "Light industrial",
  "5": "Open_Space",
  "6": "Parking",
  "7": "Academic"
}

json.dump(grid_geo, open('examples/results/corktown_geogrid.geojson', 'w'))

corktown_grid.plot()

# INITIALISE GEOGRIDDATA
geogriddata=[{"color": [
                  255,
                  255,
                  255,
                  180
                ],
                "height": 0.1,
                "id": i,
                "interactive": True,
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

#r = requests.post(output_url+'/GEOGRIDDATA', data = json.dumps(geogriddata))
#print('Geogriddata:')
#print(r)