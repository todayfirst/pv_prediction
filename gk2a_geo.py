# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:58:49 2020

@author: spins
"""

import netCDF4
import numpy as np
import os

path = u"F:\\Downloads\\b_IR3"
savepath = "F:\\Downloads\\data"
os.chdir(path)
#left_up_lon = 45.728965
#left_up_lat = 113.996417
#right_low_lat = 29.312252
#right_low_lon = 135.246740
#%%
gk2a_nc = 'gk2a_ami_le1b_ir105_ko020lc_201907250300.nc'
input_nc = netCDF4.Dataset(gk2a_nc, 'r', format = 'netcdf4')
img = input_nc.variables['image_pixel_values']
img_ds = img[:]
plt.imshow(img_ds)

#%% Bit masking
channel=img.getncattr('channel_name')
if ((channel == 'VI004') or (channel == 'VI005') or (channel == 'NR016')):
    mask = 0b0000011111111111 #11bit mask
elif ((channel == 'VI006') or (channel == 'NR013') or (channel == 'WV063')):
    mask = 0b0000111111111111 #12bit mask
elif (channel == 'SW038'):
    mask = 0b0011111111111111 #14bit mask
else:
    mask = 0b0001111111111111 #13bit mask
img_ds_masked=np.bitwise_and(img_ds,mask) 
    
#%% Georeference
from affine import Affine
import rasterio


del_lon = (138.022 - 113.985)/900
del_lat = (29.3036 - 45.7348)/900

#Define affine transform
transform = Affine.translation(113.985, 45.7348) * Affine.scale(del_lon, del_lat)
#Affine.translation(lon0, lat0)
with rasterio.open(savepath+'\\gk2a_ir3.tif', 'w', driver='GTiff',
                   dtype='uint16',
                   width=900,
                   height=900,
                   count=1,
                   crs='+proj=latlong +datum=WGS84 +type=crs',
                   transform = transform
                   ) as dst:
    dst.write(img_ds_masked, indexes=1)