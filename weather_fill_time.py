#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

def insert_row(df, row_i, value): #row_i 에 올것
    line = pd.DataFrame({"time" : value}, index = [row_i-0.5])
    df = df.append(line, ignore_index = False)
    df = df.sort_index().reset_index(drop = True)
    return df

##modify: 실험에 사용될 파일 위치 설정 

path_of_pv= "F:\\Downloads\\data\\"+"E2MS_9Site_PV_Power.csv"
#path_crop = "F:\\Downloads\\data\\"+plant_id
path_data = "F:\\Downloads\\data"
dataset = pd.read_csv(path_of_pv,sep=",", header=0)


#%% 1. Training set

dataset["time"]

cnt = 1
high = len(dataset)
b_time = dataset['time'][0]
b_i_time = int(b_time[-5:-3])
while(cnt<high):
    time = dataset['time'][cnt]
    i_time = int(time[-5:-3])
    if b_i_time == 23:
        b_i_time =-1
    if b_i_time+1 == i_time:
        cnt = cnt+1
        b_time = time
        b_i_time = i_time
        continue
    else:
        insert_time = b_time[:11]+str(b_i_time+1).zfill(2) + b_time[-3:]
        
        dataset = insert_row(dataset,cnt,insert_time)
        b_time = insert_time
        b_i_time = b_i_time+1
        cnt = cnt+1
        high = high + 1
        
        
dataset.to_csv(path_data+"//"+"PV_weather_data_new_check.csv",index = False, mode='w')




#%% 2. Test set


dataset["time"]

cnt = 1
high = len(dataset)
b_time = dataset['time'][0]
b_i_time = int(b_time[-5:-3])
while(cnt<high):
    time = dataset['time'][cnt]
    i_time = int(time[-5:-3])
    if b_i_time == 23:
        b_i_time =-1
    if b_i_time+1 == i_time:
        cnt = cnt+1
        b_time = time
        b_i_time = i_time
        continue
    else:
        insert_time = b_time[:11]+str(b_i_time+1).zfill(2) + b_time[-3:]
        
        dataset = insert_row(dataset,cnt,insert_time)
        b_time = insert_time
        b_i_time = b_i_time+1
        cnt = cnt+1
        high = high + 1
        
        
dataset.to_csv(path_data+"//"+"PV_weather_data_pred_check.csv",index = False, mode='w')

