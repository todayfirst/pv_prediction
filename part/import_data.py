# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 21:05:59 2019

@author: todayfirst
"""
import numpy as np
import pandas as pd

def run(test_mode, comsset, plant_id, minute, weather_ele):
    Pbasic_data = []
    
    path_crop = ".\\result\\"+plant_id
    
    basic_data=pd.read_csv(path_crop+"\\"+plant_id+'_dataset_with_coms_pixel.csv',sep=",", header=0)
    basic_data["coms_index"] = basic_data.index[:]
    
    if test_mode[0] ==1:
        Pbasic_data=pd.read_csv(path_crop+"\\"+plant_id+'_dataset_with_coms_pixel_test.csv',sep=",", header=0)
        Pbasic_data["coms_index"] = Pbasic_data.index[:]
        
        
    #path_weather = "F:\\Downloads\\data\\weather\\"+plant_id+"\\weather_data_new.csv"
    #path_weather_predict = "F:\\Downloads\\data\\weather\\"+plant_id+"\\weather_data_new_pred.csv"
    path_weather = "F:\\Downloads\\data\\weather\\"+plant_id+"\\weather_data_new_full.csv"
    weather = pd.read_csv(path_weather,sep=",",header=0)
    #weather = weather[240:]    
    weather.reset_index(inplace = True)
    

    #Set extents of training or test set array
    train_start = '7/25/2019 0:00'
    train_end = '9/30/2019 23:00'
    
    start_idx = basic_data["time"].loc[basic_data["time"] == train_start].index[0]
    end_idx = basic_data["time"].loc[basic_data["time"] == train_end].index[0]
    
    basic_data = basic_data[start_idx:end_idx]
    
    weather_start = '2019-07-25 0:00'
    weather_end = '2019-09-30 23:00'
    
    wstart_idx = weather["time"].loc[weather["time"] == weather_start].index[0]
    wend_idx = weather["time"].loc[weather["time"] == weather_end].index[0]
    
    Tweather = weather[wstart_idx:wend_idx]
                                  
    
    #if(len(weather)>len(basic_data)):
    #    weather = weather[:len(basic_data)] 
    #else:
    #    basic_data = basic_data[:len(weather)]
    
    basic_data.index = Tweather.index #reset index
       
    for i in weather_ele:
    #for i in range(1,10):
        basic_data[plant_id+"_"+str(i)] =Tweather[plant_id+"_"+str(i)]
    
    if test_mode[0] == 1:
        
        Pweather = pd.read_csv(path_weather,sep=",",header=0)
        #Pweather = Pweather[240:]
        Pweather.reset_index(inplace = True)
        #print(Pweather.head(10))
    
        ptrain_t = '10/1/2019 0:00'
        ptest_t = '10/31/2019 23:00'
        
        ptrain_idx = Pbasic_data["time"].loc[Pbasic_data["time"] == ptrain_t].index[0]
        ptest_idx = Pbasic_data["time"].loc[Pbasic_data["time"] == ptest_t].index[0]
        Pbasic_data = Pbasic_data[ptrain_idx:ptest_idx]
        
        pweather_start = '2019-10-01 0:00'
        pweather_end = '2019-10-31 23:00'
        
        pwstart_idx = Pweather["time"].loc[Pweather["time"] == pweather_start].index[0]
        pwend_idx = Pweather["time"].loc[Pweather["time"] == pweather_end].index[0]
    
        Pweather = Pweather[pwstart_idx:pwend_idx]

        #if(len(Pweather)>len(Pbasic_data)):
        #    Pweather = Pweather[:len(Pbasic_data)] 
        #else:
        #    Pbasic_data = Pbasic_data[:len(Pweather)]
        Pbasic_data.index = Pweather.index #reset index

        #for i in range(1,10):
        for i in weather_ele:
            Pbasic_data[plant_id+"_"+str(i)] =Pweather[plant_id+"_"+str(i)]
    '''
    if test_mode[0]==4:
        
        numofimage = len(basic_data )
        start = round(numofimage/test_mode[2]*(test_mode[1]-1))
        end = round(numofimage/test_mode[2]*(test_mode[1]))
        
        Pbasic_data = basic_data[start:end]
        basic_data = pd.concat([basic_data[:start],basic_data[end:] ])
    '''
    return (basic_data, Pbasic_data)
   