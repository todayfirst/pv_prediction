#!/usr/bin/env python
# coding: utf-8

import numpy as np
from PIL import Image
import os
import pandas as pd
import netCDF4

#import Lat2Grid
#import PIL.Image as pilimg
#import matplotlib.pyplot as plt

#Change :
# 1. Dataset header (for row and columns based on resolution)
# 2. path_of_sat for band
# 3. 

dataset = pd.read_csv("F:\\Downloads\\data\\plant_info.csv",sep=",", header=0)

for plant_n in range(1,7):
    
    plant_id = "t"+str(plant_n)
    lat, lon,r,c = [dataset["lat"][plant_n - 1], dataset["lon"][plant_n - 1],
                    dataset["r_2"][plant_n - 1], dataset["c_2"][plant_n - 1]]
    ##Omit 25kW (t2 and t6)
    #r,c  = Lat2Grid.toGrid(lat,lon)
    #print(r,c)
    
    ##b_red, b_NIR2,b_SWIR,b_IR3,b_IR4,b_IR5
    path_of_sat = "F:\\Downloads\\b_red"
    path_to_crop = "F:\\Downloads\\data\\"+plant_id+"\\crop_image"
    
    file_list = os.listdir(path_of_sat )
    file_list_py = [file for file in file_list if file.endswith(".nc")]
    #print ("file_list: {}".format(file_list_py))
    
    #천리안 파일
    cnt = 0
    
    for (path, dir, files) in os.walk(path_of_sat):
        for filename in files:
           # if cnt ==5:
           #     break
            ext = os.path.splitext(filename)[-1]
            ex1 = os.path.splitext(filename)[-2]
           #년 print(ex1[-12:-8])
            #월 print(ex1[-8:-6])
            #일print(ex1[-6:-4])
            if ext == '.nc':
                #print("%s/%s" % (path, filename))
                gk2a_nc = path+"\\"+filename
                input_nc = netCDF4.Dataset(gk2a_nc, 'r', format = 'netcdf4')
                img = np.array(input_nc.variables['image_pixel_values'])
                #img_arr = np.ndarray.astype(img,dtype='float32')
                bdata_np_reshape_crop = img[c-60:c+61, r-60:r+61]
                cropped_img = Image.fromarray(bdata_np_reshape_crop)
                #bdata_np_reshape_crop = np.resize(c-30, r-30, c+31, r+31 )
                #bdata_np_reshape_crop= np.array(bdata_np_reshape)
                
                print(filename)
                #plt.imshow(bdata_np_reshape)
                #plt.show()
                cnt=cnt+1
                dirname = path_to_crop+"\\"+ex1[-12:-8]+"\\M"+ex1[-8:-6]+"\\D"+ex1[-6:-4]
    
                if not os.path.isdir(dirname):
                    if not os.path.isdir(path_to_crop+"\\"+ex1[-12:-8]):
                        os.mkdir(path_to_crop+"\\"+ex1[-12:-8])
                    if not os.path.isdir(path_to_crop+"\\"+ex1[-12:-8]+"\\M"+ex1[-8:-6]):
                        os.mkdir(path_to_crop+"\\"+ex1[-12:-8]+"\\M"+ex1[-8:-6])    
                    os.mkdir(dirname)
                    
                cropped_img.save(dirname +"\\crop_"+ex1+".tif")
            #    print(shape(bdata_np_reshape_crop))
                if cnt%1000==0:
                    print("SAVE OK"+str(cnt)+" : "+dirname +"\\crop_"+ex1+".tif")
        
        #np.savetxt("C:\\Users\\todayfirst\\Desktop\\skt\\201908 preprocessing\\crop\\cropped_"+file_list_py[i], bdata_np_reshape_crop)
