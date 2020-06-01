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

nrows = 92
ncols = 80

rotation = 23


cell_size = 25
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
interactive_region=json.load(open('examples/interactive_regions/corktown_interactive_area.geojson'))
corktown_grid.set_web_interactive_region(interactive_region)

parcel_data=json.load(open('examples/land_use_data/corktown_parcels_cs_types.geojson'))
new_static_blds_data=json.load(open('examples/land_use_data/corktown_static_new.geojson'))

for feat in parcel_data['features']:
    feat['properties']['static_new']=False
    
parcel_data['features'].extend(new_static_blds_data['features'])

parcel_properties={'type': {'from':'CS_LU', 'default': 'None'}, 
                   'height': {'from':'effective_num_floors', 'default': 0},
                   'year': {'from':'year_built', 'default': 0},
                   'static_new': {'from':'static_new', 'default': False}
                   }
corktown_grid.set_grid_properties_from_shapefile(parcel_data, parcel_properties)



grid_geo=corktown_grid.get_grid_geojson(add_properties={})

# =============================================================================
#  Add types for web-based editing to header
# =============================================================================
types=json.load(open('examples/type_definitions/corktown_types.json'))
grid_geo['properties']['types']=types

# =============================================================================
# # INITIALISE GEOGRIDDATA
## =============================================================================
#geogriddata=[{"color": [
#                  0,
#                  0,
#                  0,
#                  0
#                ],
#                "height": 0,
#                "id": i,
#                "interactive": grid_geo['features'][i]['properties']['interactive'],
#                "land_use": grid_geo['features'][i]['properties']['land_use'],
#                "name": "empty",
#                "tui_id": None
#              } for i in range(len(grid_geo['features']))]
geogriddata=[]
for ic, cell in enumerate(grid_geo['features']):
    this_geogrid_cell={}
    this_geogrid_cell['name']=cell['properties']['type']
#    this_geogrid_cell['name']="empty"
    this_geogrid_cell['color']=types[cell['properties']['type']]['color']
#    this_geogrid_cell['color']=[0,0,0,0]
    this_geogrid_cell['interactive']=cell['properties']['interactive']
    this_geogrid_cell['height']=cell['properties']['height']
    this_geogrid_cell['id']=ic
    this_geogrid_cell['tui_id']=None
    geogriddata.append(this_geogrid_cell)

#json.dump(geogriddata, open('../Scenarios/ford_base.json', 'w'))    
    
# =============================================================================
# post to cityIO
# =============================================================================
output_url='https://cityio.media.mit.edu/api/table/update/{}'.format(table_name)
r = requests.post(output_url+'/GEOGRID', data = json.dumps(grid_geo))
print('Geogrid:')
print(r)

json.dump(grid_geo, open('examples/results/corktown_geogrid.geojson', 'w'))

#corktown_grid.plot()
#
r = requests.post(output_url+'/GEOGRIDDATA', data = json.dumps(geogriddata))
print('Geogriddata:')
print(r)