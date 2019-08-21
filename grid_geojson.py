#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 18:57:59 2019

@author: doorleyr
"""
import math

def deg_to_rad(deg):
    return deg*math.pi/180

def rad_to_deg(rad):
    return rad*180/math.pi

def point_at_distance_and_bearing_from(point_1, bearing, distance):
    EARTH_RADIUS_M=6.371e6
    Ad=distance/EARTH_RADIUS_M
    la1=deg_to_rad(point_1['lat'])
    lo1=deg_to_rad(point_1['lon'])
    bearing_rad=deg_to_rad(bearing)
    la2= math.asin(math.sin(la1) * math.cos(Ad)  + 
                      math.cos(la1) * math.sin(Ad) * math.cos(bearing_rad))
    lo2= lo1+ math.atan2(math.sin(bearing_rad) * math.sin(Ad) * math.cos(la1),
                         math.cos(Ad)-math.sin(la1)*math.sin(la2))
    point_2={'lon': rad_to_deg(lo2), 'lat': rad_to_deg(la2)}
    return point_2
    

class Grid():
    def __init__(self, top_left_lon, top_left_lat, rotation,
                 cell_size, nrows, ncols):
        """
        Takes the properties of the grid and using the Haversine formula, 
        computes the location of the top-right corner. Then projects
        to spatial coordinates in order to find the locations of the rest of 
        the grid cells
        """        
        top_left_lon_lat={'lon': top_left_lon, 'lat': top_left_lat}
        bearing_across_grid=(90-rotation+360)%360
        bearing_down_grid=(180-rotation+360)%360
        top_right_lon_lat=point_at_distance_and_bearing_from(top_left_lon_lat, 
                                                             bearing_across_grid, 
                                                             ncols*cell_size)
        bottom_left_lon_lat=point_at_distance_and_bearing_from(top_left_lon_lat, 
                                                         bearing_down_grid, 
                                                         nrows*cell_size)
        self.delta_ll_across={'lon': (top_right_lon_lat['lon']-top_left_lon_lat['lon'])/ncols,
                       'lat': (top_right_lon_lat['lat']-top_left_lon_lat['lat'])/ncols}
        self.delta_ll_down={'lon': (bottom_left_lon_lat['lon']-top_left_lon_lat['lon'])/nrows,
                       'lat': (bottom_left_lon_lat['lat']-top_left_lon_lat['lat'])/nrows}
        self.all_cells_top_left=[{'lon':top_left_lon_lat['lon']+i*self.delta_ll_across['lon']+
                    j*self.delta_ll_down['lon'],
                    'lat':top_left_lon_lat['lat']+i*self.delta_ll_across['lat']+
                    j*self.delta_ll_down['lat']
                    } for j in range(nrows) for i in range(ncols)]
    def get_grid_geojson(self, properties):
        """
        Takes the pre-computed locations of the top-left corner of every grid cell
        and creates a corresponding Multi-Polygon geojson object
        """ 
        features=[]
        for i, g in enumerate(self.all_cells_top_left):
            coords=[[g['lon'], g['lat']],
                    [g['lon']+self.delta_ll_down['lon'], g['lat']+self.delta_ll_down['lat']],
                    [g['lon']+self.delta_ll_across['lon']+self.delta_ll_down['lon'], g['lat']+
                     self.delta_ll_across['lat']+self.delta_ll_down['lat']],
                    [g['lon']+self.delta_ll_across['lon'],g['lat']+self.delta_ll_across['lat']], 
                    [g['lon'], g['lat']]]
            features.append({'type': 'Feature',
                             'geometry':{'type': 'Polygon', 'coordinates': [coords]},
                             'properties': {p: properties[p][i] for p in properties}})
        return {'type': 'FeatureCollection',
                        'features': features}
        



