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

table_name='grasbrook'

# =============================================================================
# Composite Grid
# =============================================================================
top_left_lon = 10.006775
top_left_lat = 53.537894

nrows = 44
ncols = 78

rotation = 145.5


cell_size = 16
crs_epsg = '31468'

tui_top_left_row_index=13
tui_top_left_col_index=13
tui_num_interactive_rows=10
tui_num_interactive_cols=10



grasbrook_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

grasbrook_grid.add_tui_interactive_cells(tui_top_left_row_index, tui_top_left_col_index,
                                  tui_num_interactive_rows, tui_num_interactive_cols)
grasbrook_grid.plot()
# =============================================================================
# Get Land Uses
# =============================================================================
land_use=json.load(open('examples/land_use_data/grasbrook_osm_landuse.geojson'))
lu_property='fclass'
grasbrook_grid.get_land_uses(land_use, lu_property)

grid_geo=grasbrook_grid.get_grid_geojson(add_properties={})

# =============================================================================
# Set some cells interactivity to False based on Land-Use
# =============================================================================

for f in grid_geo['features']:
    if f['properties']['land_use'] in ['scrub', 'None']:
        f['properties']['interactive']=False

json.dump(grid_geo, open('examples/results/grasbrook_geogrid.geojson', 'w'))

# =============================================================================
# post to cityIO
# =============================================================================
output_url='https://cityio.media.mit.edu/api/table/update/{}'.format(table_name)
r = requests.post(output_url+'GEOGRID', data = json.dumps(grid_geo))
print('Geogrid:')
print(r)









