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

# Active Area
top_left_lon = 19.050979614257812
top_left_lat = 47.43630292431787

nrows = 15
ncols = 15

# rotation
rotation = 260
# cell size
cell_size = 50

# projection system
crs_epsg = '3836'

col_margin_left=0 # columns to add to left of interactive grid to create full grid
row_margin_top=0 # rows to add to top of interactive grid to create full grid
full_cell_width=ncols # total num columns in full grid
full_cell_height=nrows # total num rows in full grid


# First create the interactive grid
csepel_grid = Grid(top_left_lon, top_left_lat, rotation,
                      crs_epsg, cell_size, nrows, ncols)

# then extend it to create the full grid
# Same as the interactive so extend by 0 cells
csepel_grid.extend_int_grid_to_full(col_margin_left,  row_margin_top, 
                                    full_cell_width, full_cell_height)
csepel_grid.plot()


grid_geo=csepel_grid.get_grid_geojson(add_properties={'height': [10]*len(
        csepel_grid.grid_coords_ll)})

# post to cityIO
output_url='https://cityio.media.mit.edu/api/table/update/csepel/meta_grid'
r = requests.post(output_url, data = json.dumps(grid_geo))
print(r)



