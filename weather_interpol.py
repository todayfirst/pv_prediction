#!/usr/bin/env python
# coding: utf-8

#%% 1. Training set

import pandas as pd
import numpy as np

for plant_n in range(1,7):
    plant_id = "t"+str(plant_n)
    path_of_weather= "F:\\Downloads\data\\weather\\"+plant_id+"\\"

    weather_ele = [1,2,3,4,7,8,9]
    
    print(plant_n)
    
    ds = pd.read_csv(path_of_weather+"weather_data_new.csv",sep=",", header=0)
    cnt =3
    while(cnt<len(ds)):
        if (cnt/3) % 300==0:
            print(ds["time"][cnt])
        for i in weather_ele:
            if np.isnan(ds.iloc[cnt-3,[i]][0]) or np.isnan(ds.iloc[cnt,[i]][0]):
    
                continue
            else:
                ds.iloc[cnt-2,[i]] = float(ds.iloc[cnt-3,[i]][0])*2/3 + float(ds.iloc[cnt,[i]][0])/3
                ds.iloc[cnt-1,[i]] = float(ds.iloc[cnt-3,[i]][0])*1/3 + float(ds.iloc[cnt,[i]][0])*2/3  
        cnt = cnt+3
    
    ds.to_csv(path_of_weather+"weather_data_new.csv",index = False, mode='w')
    ds.head(30)



#%%  2. Test set
    
import pandas as pd
import numpy as np

for plant_n in range(1,7):
    plant_id = "t"+str(plant_n)
    path_of_weather= "F:\\Downloads\data\\weather\\"+plant_id+"\\"

    weather_ele = [1,2,3,4,7,8,9]
    
    print(plant_n)

    ds = pd.read_csv(path_of_weather+"weather_data_new_pred.csv",sep=",", header=0)
    cnt =3
    while(cnt<len(ds)):
        if (cnt/3) % 300==0:
            print(ds["time"][cnt])
        for i in weather_ele:
            if np.isnan(ds.iloc[cnt-3,[i]][0]) or np.isnan(ds.iloc[cnt,[i]][0]):
    
                continue
            else:
                ds.iloc[cnt-2,[i]] = float(ds.iloc[cnt-3,[i]][0])*2/3 + float(ds.iloc[cnt,[i]][0])/3
                ds.iloc[cnt-1,[i]] = float(ds.iloc[cnt-3,[i]][0])*1/3 + float(ds.iloc[cnt,[i]][0])*2/3  
        cnt = cnt+3
    ds.to_csv(path_of_weather+"weather_data_new_pred.csv",index = False, mode='w')
    ds.head(30)
