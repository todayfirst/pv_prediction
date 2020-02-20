# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 13:04:13 2020

@author: spins
"""

import pandas as pd
import numpy as np
import os
import rasterio as rio

#%%
path_geo = "F:\Downloads\data"

# Georeference GK2A to grid (similar to lat2grid)

os.chdir(path_geo)

gk2a_data_500 = pd.read_csv('LATLON_KO_500.txt', sep="\t", header = None)
gk2a_data_1000 = pd.read_csv('LATLON_KO_1000.txt', sep="\t", header = None)
gk2a_data_2000 = pd.read_csv('LATLON_KO_2000.txt', sep="\t", header = None)

gk2a_data_500_lat = np.asarray(gk2a_data_500.iloc[:,0])
gk2a_data_500_lon = np.asarray(gk2a_data_500.iloc[:,1])
gk2a_data_1000_lat = np.asarray(gk2a_data_1000.iloc[:,0])
gk2a_data_1000_lon = np.asarray(gk2a_data_1000.iloc[:,1])
gk2a_data_2000_lat = np.asarray(gk2a_data_2000.iloc[:,0])
gk2a_data_2000_lon = np.asarray(gk2a_data_2000.iloc[:,1])

gk2a_500_lat = np.reshape(gk2a_data_500_lat, (3600,3600), order='C')
gk2a_500_lon = np.reshape(gk2a_data_500_lon, (3600,3600), order='C')
gk2a_1000_lat = np.reshape(gk2a_data_1000_lat, (1800,1800), order='C')
gk2a_1000_lon = np.reshape(gk2a_data_1000_lon, (1800,1800), order='C')
gk2a_2000_lat = np.reshape(gk2a_data_2000_lat, (900,900), order='C')
gk2a_2000_lon = np.reshape(gk2a_data_2000_lon, (900,900), order='C')

#%% Find pixel coordinates
os.chdir(result+'\\path_geo)
#coordinates order : 순천, 창녕, 거창, 익산, 안동, 평창 (t1,t3,t4,t5,t7,t8)

coordinates = (
    (127.5377069,34.9137221),
    (128.4111392,35.50809684),
    (127.8331163,35.74963254),
    (127.0206549,36.13259121),
    (128.7022764,36.68504634),
    (128.3942227,37.42644904),
    (128.7022764,36.68504634)
)

# Open gk2a images to find pixel location

with rio.open('gk2a_red.tif') as dataset:
    # Loop through  list of coords
    for i, (lon, lat) in enumerate(coordinates):
        # Get pixel (r,c) from map coordinates
        c, r = dataset.index(lon, lat)
        print('Pixel Y, X coords: {}, {}'.format(c, r))




