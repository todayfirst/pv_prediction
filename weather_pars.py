#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


for plant_n in range(1,7):
    plant_id = "t"+str(plant_n)
    path_of_weather= "F:\\Downloads\data\\weather\\"+plant_id+"\\"
    #path_crop = "F:\\Downloads\\data\\"+plant_id
    #path_data = "F:\\Downloads\\data"
    
    print(plant_n)
    
    def Khour2GMT(Ky,Km,Kd,Kh):
        Gh = Kh-9
        Gd = Kd
        Gm = Km
        Gy = Ky
        if Gh<0:
            Gh = Gh+24
            Gd = Gd-1
        if Gd<1:
            Gd = Gd+30
            Gm = Gm-1
            if Gm==1 or Gm==3 or Gm==5 or Gm==7 or Gm==8 or Gm==10 or Gm==0:
                Gd = Gd+1
            if Gm==2: 
                Gd = Gd-2
                if Gy%4==0 and not(Gy%100==0):
                    Gd=Gd+1
        if Gm == 0:
            Gm = 12
            Gy = Gy-1
        
        return(Gy, Gm, Gd, Gh)
    def GMT2Khour(Gy, Gm, Gd, Gh):
        Kh = Gh+9
        Kd = Gd
        Km = Gm
        Ky = Gy
        if Kh>23:
            Kh = Kh-24
            Kd = Kd+1
            if Kd>31:
                Kd = 1
                Km = Km+1
                if Km == 13:
                    Km =1
                    Ky = Ky+1
            elif Kd==31:
                if Km==4 or Km==6 or Km==9 or Km==11:
                    Km = Km+1
                    Kd = 1
            elif Km==2 and Kd==30:
                Kd = 1
                Km = Km+1
            elif Km==2 and Kd==29:        
                if not(Ky%4==0 and not(Ky%100==0)):
                    Kd = 1
                    Km = Km+1
    
        return(Ky,Km,Kd,Kh)
    
    def insert_row(df, row_i, value): #row_i 에 올것
        line = pd.DataFrame({"time" : value}, index = [row_i-0.5])
        df = df.append(line, ignore_index = False)
        df = df.sort_index().reset_index(drop = True)
        return df
    
    #ds = pd.read_csv(path_of_weather+"weather_data_new.csv",sep=",", header=0)
    ds = pd.DataFrame()
    dt_index = pd.date_range(start='20190724',end = '20190930')
    dt_list = dt_index.strftime("%Y-%m-%d")
    
    ds["time"]=dt_list
    ds.head(100)
    
    
    cnt = 0
    high = len(ds)*24
    i_time=0
    while(cnt<high):
        time = ds['time'][cnt]
        print(time)
        if len(time)==10:
            ds["time"][cnt] = time + " 0:00"
            continue
        hour = int(time[-5:-3])
        if hour==23:
            cnt = cnt+1
        else:
            time = time[:10]+" "+str(hour+1)+":00"
            ds = insert_row(ds,cnt+1,time)
            cnt= cnt+1
        
    for num in range(1,10):
        ds[plant_id+"_"+str(num)] = np.nan
        ds.head(20)
    
    
    
    def Nextday(Ky, Km, Kd, Kh):
        if Kh>23:
            Kh = Kh-24
            Kd = Kd+1
            if Kd>31:
                Kd = 1
                Km = Km+1
                if Km == 13:
                    Km =1
                    Ky = Ky+1
            elif Kd==31:
                if Km==4 or Km==6 or Km==9 or Km==11:
                    Km = Km+1
                    Kd = 1
            elif Km==2 and Kd==30:
                Kd = 1
                Km = Km+1
            elif Km==2 and Kd==29:        
                if not(Ky%4==0 and not(Ky%100==0)):
                    Kd = 1
                    Km = Km+1
    
        return(Ky,Km,Kd,Kh)
    
    
    for num in range(1,10):
        Gy=2019
        Gm = 7
        Sd = 24 ### Sd (Set to n-1 of first day)
        
        dataset = pd.read_csv(path_of_weather+plant_id+"_"+str(num)+".csv",sep=",", header=0)
        first_Sd = True
        cnt = 0
        dscnt = 0
        det = False
        while(cnt<len(dataset) and dscnt < len(ds)):
            if cnt%3000==0:
                print(str(num)+" : "+ ds["time"][dscnt])
            while(first_Sd and (int(dataset.iloc[cnt,[0]][0]) < Sd)):
                cnt = cnt+1
                print(int(dataset.iloc[cnt,[0]][0]))
            first_Sd = False
            
            if cnt==0:
                Gd = 24 ### set to first date (n)
                Gh = (dataset.iloc[cnt,[1]][0]/100+dataset.iloc[cnt,[2]][0])
                Gy1, Gm1 ,Gd1, Gh1 = Nextday(Gy, Gm, Gd, Gh)
                Ky, Km, Kd, Kh = GMT2Khour(Gy1, Gm1, Gd1, Gh1)
                time = str(Ky)+"-"+str(Km).zfill(2)+"-"+str(Kd).zfill(2)+" "+str(int(Kh))+":00"
                print(time)
    
                while(dscnt<len(ds)):
                    
                    if ds["time"][dscnt] == time:
                        ds[plant_id+"_"+str(num)][dscnt] = float(dataset.iloc[cnt,[3]])
                        #print(cnt)
                        
                        break
                    else :
                        dscnt= dscnt+1
                cnt = cnt+1
            else:
                
                if len(((dataset.iloc[cnt,[0]][0])))>8:
                    Start = dataset.iloc[cnt,[0]][0]
                    Gy = int(Start[-9:-5])
                    Gm =  int(Start[-5:-3])
                    Sd = int(Start[-3:-1])
                    cnt= cnt+1
                    det = True
                    continue
                else:
                    if det or not(dataset.iloc[cnt,[1]][0]==dataset.iloc[cnt-1,[1]][0]):
    
                        Gd = int(dataset.iloc[cnt,[0]][0])
                        Gh = dataset.iloc[cnt,[1]][0]/100+dataset.iloc[cnt,[2]][0]
                        Gy1, Gm1 ,Gd1, Gh1 = Nextday(Gy, Gm, Gd, Gh)
                        
                        Ky, Km, Kd, Kh = GMT2Khour(Gy1, Gm1, Gd1, Gh1)
                        time = str(Ky)+"-"+str(Km).zfill(2)+"-"+str(Kd).zfill(2)+" "+str(int(Kh))+":00"
                       # print(time)
    
                        while(dscnt<len(ds)):
    
                            if ds["time"][dscnt] == time:
                                ds[plant_id+"_"+str(num)][dscnt] = float(dataset.iloc[cnt,[3]])
                                #print(cnt)
                                break
                            else :
                                dscnt= dscnt+1

                        det = False
                    cnt = cnt+1
    
    
    ds.head(30)
    ds.to_csv(path_of_weather+"weather_data_new.csv",index = False, mode='w')
    


#print(dataset.iloc[0,[1]][0]/100)

#%%

import pandas as pd
import numpy as np


for plant_n in range(1,7):
    plant_id = "t"+str(plant_n)
    path_of_weather= "F:\\Downloads\data\\weather\\"+plant_id+"\\"
    #path_crop = "F:\\Downloads\\data\\"+plant_id
    #path_data = "F:\\Downloads\\data"
    
    print(plant_n)
    
    def Khour2GMT(Ky,Km,Kd,Kh):
        Gh = Kh-9
        Gd = Kd
        Gm = Km
        Gy = Ky
        if Gh<0:
            Gh = Gh+24
            Gd = Gd-1
        if Gd<1:
            Gd = Gd+30
            Gm = Gm-1
            if Gm==1 or Gm==3 or Gm==5 or Gm==7 or Gm==8 or Gm==10 or Gm==0:
                Gd = Gd+1
            if Gm==2: 
                Gd = Gd-2
                if Gy%4==0 and not(Gy%100==0):
                    Gd=Gd+1
        if Gm == 0:
            Gm = 12
            Gy = Gy-1
        
        return(Gy, Gm, Gd, Gh)
    def GMT2Khour(Gy, Gm, Gd, Gh):
        Kh = Gh+9
        Kd = Gd
        Km = Gm
        Ky = Gy
        if Kh>23:
            Kh = Kh-24
            Kd = Kd+1
            if Kd>31:
                Kd = 1
                Km = Km+1
                if Km == 13:
                    Km =1
                    Ky = Ky+1
            elif Kd==31:
                if Km==4 or Km==6 or Km==9 or Km==11:
                    Km = Km+1
                    Kd = 1
            elif Km==2 and Kd==30:
                Kd = 1
                Km = Km+1
            elif Km==2 and Kd==29:        
                if not(Ky%4==0 and not(Ky%100==0)):
                    Kd = 1
                    Km = Km+1
    
        return(Ky,Km,Kd,Kh)
    
    def insert_row(df, row_i, value): #row_i 에 올것
        line = pd.DataFrame({"time" : value}, index = [row_i-0.5])
        df = df.append(line, ignore_index = False)
        df = df.sort_index().reset_index(drop = True)
        return df
    
    #ds = pd.read_csv(path_of_weather+"weather_data_new.csv",sep=",", header=0)
    ds = pd.DataFrame()
    dt_index = pd.date_range(start='20191001',end = '20191101')
    dt_list = dt_index.strftime("%Y-%m-%d")
    
    ds["time"]=dt_list
    ds.head(100)
    
    
    cnt = 0
    high = len(ds)*24
    i_time=0
    while(cnt<high):
        time = ds['time'][cnt]
        print(time)
        if len(time)==10:
            ds["time"][cnt] = time + " 0:00"
            continue
        hour = int(time[-5:-3])
        if hour==23:
            cnt = cnt+1
        else:
            time = time[:10]+" "+str(hour+1)+":00"
            ds = insert_row(ds,cnt+1,time)
            cnt= cnt+1
        
    for num in range(1,10):
        ds[plant_id+"_"+str(num)] = np.nan
        ds.head(20)
    
    
    
    def Nextday(Ky, Km, Kd, Kh):
        if Kh>23:
            Kh = Kh-24
            Kd = Kd+1
            if Kd>31:
                Kd = 1
                Km = Km+1
                if Km == 13:
                    Km =1
                    Ky = Ky+1
            elif Kd==31:
                if Km==4 or Km==6 or Km==9 or Km==11:
                    Km = Km+1
                    Kd = 1
            elif Km==2 and Kd==30:
                Kd = 1
                Km = Km+1
            elif Km==2 and Kd==29:        
                if not(Ky%4==0 and not(Ky%100==0)):
                    Kd = 1
                    Km = Km+1
    
        return(Ky,Km,Kd,Kh)
    
    
    for num in range(1,10):
        Gy=2019
        Gm = 10
        Sd = 1 ### Sd (Set to n-1 of first day)
        
        dataset = pd.read_csv(path_of_weather+plant_id+"_"+str(num)+".csv",sep=",", header=0)
        first_Sd = True
        cnt = 0
        dscnt = 0
        det = False
        while(cnt<len(dataset) and dscnt < len(ds)):
            if cnt%3000==0:
                print(str(num)+" : "+ ds["time"][dscnt])
            while(first_Sd and (int(dataset.iloc[cnt,[0]][0]) < Sd)):
                cnt = cnt+1
                print(int(dataset.iloc[cnt,[0]][0]))
            first_Sd = False
            
            if cnt==0:
                Gd = 1 ### set to first date (n)
                Gh = (dataset.iloc[cnt,[1]][0]/100+dataset.iloc[cnt,[2]][0])
                Gy1, Gm1 ,Gd1, Gh1 = Nextday(Gy, Gm, Gd, Gh)
                Ky, Km, Kd, Kh = GMT2Khour(Gy1, Gm1, Gd1, Gh1)
                time = str(Ky)+"-"+str(Km).zfill(2)+"-"+str(Kd).zfill(2)+" "+str(int(Kh))+":00"
                print(time)
    
                while(dscnt<len(ds)):
                    
                    if ds["time"][dscnt] == time:
                        ds[plant_id+"_"+str(num)][dscnt] = float(dataset.iloc[cnt,[3]])
                        #print(cnt)
                        
                        break
                    else :
                        dscnt= dscnt+1
                cnt = cnt+1
            else:
                
                if len(((dataset.iloc[cnt,[0]][0])))>8:
                    Start = dataset.iloc[cnt,[0]][0]
                    Gy = int(Start[-9:-5])
                    Gm =  int(Start[-5:-3])
                    Sd = int(Start[-3:-1])
                    cnt= cnt+1
                    det = True
                    continue
                else:
                    if det or not(dataset.iloc[cnt,[1]][0]==dataset.iloc[cnt-1,[1]][0]):
    
                        Gd = int(dataset.iloc[cnt,[0]][0])
                        Gh = dataset.iloc[cnt,[1]][0]/100+dataset.iloc[cnt,[2]][0]
                        Gy1, Gm1 ,Gd1, Gh1 = Nextday(Gy, Gm, Gd, Gh)
                        
                        Ky, Km, Kd, Kh = GMT2Khour(Gy1, Gm1, Gd1, Gh1)
                        time = str(Ky)+"-"+str(Km).zfill(2)+"-"+str(Kd).zfill(2)+" "+str(int(Kh))+":00"
                       # print(time)
    
                        while(dscnt<len(ds)):
    
                            if ds["time"][dscnt] == time:
                                ds[plant_id+"_"+str(num)][dscnt] = float(dataset.iloc[cnt,[3]])
                                #print(cnt)
                                break
                            else :
                                dscnt= dscnt+1

                        det = False
                    cnt = cnt+1
    
    
    ds.head(30)
    ds.to_csv(path_of_weather+"weather_data_new_pred.csv",index = False, mode='w')
    





#%%
############################ Test data ############################
############################## 5~8월 ##############################

import pandas as pd
import numpy as np


for plant_n in range(1,7):
    plant_id = "t"+str(plant_n)
    path_of_weather= "F:\\Downloads\data\\weather\\"+plant_id+"\\"
    #path_crop = "F:\\Downloads\\data\\"+plant_id
    #path_data = "F:\\Downloads\\data"
    
    print(plant_n)
    
    def Khour2GMT(Ky,Km,Kd,Kh):
        Gh = Kh-9
        Gd = Kd
        Gm = Km
        Gy = Ky
        if Gh<0:
            Gh = Gh+24
            Gd = Gd-1
        if Gd<1:
            Gd = Gd+30
            Gm = Gm-1
            if Gm==1 or Gm==3 or Gm==5 or Gm==7 or Gm==8 or Gm==10 or Gm==0:
                Gd = Gd+1
            if Gm==2: 
                Gd = Gd-2
                if Gy%4==0 and not(Gy%100==0):
                    Gd=Gd+1
        if Gm == 0:
            Gm = 12
            Gy = Gy-1
        
        return(Gy, Gm, Gd, Gh)
    
    def GMT2Khour(Gy, Gm, Gd, Gh):
        Kh = Gh+9
        Kd = Gd
        Km = Gm
        Ky = Gy
        if Kh>23:
            Kh = Kh-24
            Kd = Kd+1
            if Kd>31:
                Kd = 1
                Km = Km+1
                if Km == 13:
                    Km =1
                    Ky = Ky+1
            elif Kd==31:
                if Km==4 or Km==6 or Km==9 or Km==11:
                    Km = Km+1
                    Kd = 1
            elif Km==2 and Kd==30:
                Kd = 1
                Km = Km+1
            elif Km==2 and Kd==29:        
                if not(Ky%4==0 and not(Ky%100==0)):
                    Kd = 1
                    Km = Km+1
    
        return(Ky,Km,Kd,Kh)
    
    def insert_row(df, row_i, value): #row_i 에 올것
        line = pd.DataFrame({"time" : value}, index = [row_i-0.5])
        df = df.append(line, ignore_index = False)
        df = df.sort_index().reset_index(drop = True)
        return df
    
    #ds = pd.read_csv(path_of_weather+"weather_data_new.csv",sep=",", header=0)
    ds = pd.DataFrame()
    dt_index = pd.date_range(start='20190724',end = '20190930')
    dt_list = dt_index.strftime("%Y-%m-%d")
    
    ds["time"]=dt_list
    ds.head(100)
    
    
    cnt = 0
    high = len(ds)*24
    i_time=0
    while(cnt<high):
        time = ds['time'][cnt]
        print(time)
        if len(time)==10:
            ds["time"][cnt] = time + " 0:00"
            continue
        hour = int(time[-5:-3])
        if hour==23:
            cnt = cnt+1
        else:
            time = time[:10]+" "+str(hour+1)+":00"
            ds = insert_row(ds,cnt+1,time)
            cnt= cnt+1
        
    for num in range(1,10):
        ds[plant_id+"_"+str(num)] = np.nan
        ds.head(20)
    
    def Nextday(Ky, Km, Kd, Kh):
        if Kh>23:
            Kh = Kh-24
            Kd = Kd+1
            if Kd>31:
                Kd = 1
                Km = Km+1
                if Km == 13:
                    Km =1
                    Ky = Ky+1
            elif Kd==31:
                if Km==4 or Km==6 or Km==9 or Km==11:
                    Km = Km+1
                    Kd = 1
            elif Km==2 and Kd==30:
                Kd = 1
                Km = Km+1
            elif Km==2 and Kd==29:        
                if not(Ky%4==0 and not(Ky%100==0)):
                    Kd = 1
                    Km = Km+1
    
        return(Ky,Km,Kd,Kh)

    for num in range(1,10):
        Gy=2019
        Gm = 10
        Sd = 0
        
        dataset = pd.read_csv(path_of_weather+plant_id+"_"+str(num)+".csv",sep=",", header=0)
        cnt = 0
        dscnt = 0
        det = False
        while(cnt<len(dataset)):
            if cnt%3000==0:
                print(str(num)+" : "+ ds["time"][dscnt])
            if cnt==0:
                Gd = 1
                
                Gh = (dataset.iloc[cnt,[1]][0]/100+dataset.iloc[cnt,[2]][0])
                Gy1, Gm1 ,Gd1, Gh1 = Nextday(Gy, Gm, Gd, Gh)
                Ky, Km, Kd, Kh = GMT2Khour(Gy1, Gm1, Gd1, Gh1)
                time = str(Ky)+"-"+str(Km).zfill(2)+"-"+str(Kd).zfill(2)+" "+str(int(Kh))+":00"
                #print(time)
    
                while(dscnt<len(ds)):
                    
                    if ds["time"][dscnt] == time:
                        ds[plant_id+"_"+str(num)][dscnt] = float(dataset.iloc[cnt,[3]])
                        #print(cnt)
    
                        break
                    else :
                        dscnt= dscnt+1
                cnt = cnt+1
            else:
                
                if len(((dataset.iloc[cnt,[0]][0])))>8:
                    Start = dataset.iloc[cnt,[0]][0]
                    Gy = int(Start[-9:-5])
                    Gm =  int(Start[-5:-3])
                    Sd = int(Start[-3:-1])-1
                    cnt= cnt+1
                    det = True
                    continue
                else:
                    if det or not(dataset.iloc[cnt,[1]][0]==dataset.iloc[cnt-1,[1]][0]):
    
                        Gd = Sd + int(dataset.iloc[cnt,[0]][0])
                        Gh = dataset.iloc[cnt,[1]][0]/100+dataset.iloc[cnt,[2]][0]
                        Gy1, Gm1 ,Gd1, Gh1 = Nextday(Gy, Gm, Gd, Gh)
                        
                        Ky, Km, Kd, Kh = GMT2Khour(Gy1, Gm1, Gd1, Gh1)
                        time = str(Ky)+"-"+str(Km).zfill(2)+"-"+str(Kd).zfill(2)+" "+str(int(Kh))+":00"
                       # print(time)
    
                        while(dscnt<len(ds)):
    
                            if ds["time"][dscnt] == time:
                                ds[plant_id+"_"+str(num)][dscnt] = float(dataset.iloc[cnt,[3]])
                              #  print(cnt)
                                break
                            else :
                                dscnt= dscnt+1
                        det = False
                    cnt = cnt+1


    ds = pd.DataFrame()
    #ds = pd.read_csv(path_of_weather+"weather_data_new_pred.csv",sep=",", header=0)
    dt_index = pd.date_range(start='20191001',end = '20191101')
    dt_list = dt_index.strftime("%Y-%m-%d")
    ds["time"]=dt_list
    ds.head(10)

    cnt = 0
    high = len(ds)*24
    i_time=0
    while(cnt<high):
        time = ds['time'][cnt]
        if len(time)==10:
            ds["time"][cnt] = time + " 0:00"
            continue
        hour = int(time[-5:-3])
        if hour==23:
            cnt = cnt+1
        else:
            time = time[:10]+" "+str(hour+1)+":00"
            ds = insert_row(ds,cnt+1,time)
            cnt= cnt+1

    ds.head(30)

    for num in range(1,10):
        ds[plant_id+"_"+str(num)] = np.nan

    
    for num in range(1,10):
        Gy=2019
        Gm = 10
        Sd = 0
        
        dataset = pd.read_csv(path_of_weather+plant_id+"_"+str(num)+".csv",sep=",", header=0)
        cnt = 0
        dscnt = 0
        det = False
        while(cnt<len(dataset)):
            if cnt%3000==0:
                print(str(num)+" : "+ ds["time"][dscnt])
            if cnt==0:
                Gd = 1
                
                Gh = (dataset.iloc[cnt,[1]][0]/100+dataset.iloc[cnt,[2]][0])
                Gy1, Gm1 ,Gd1, Gh1 = Nextday(Gy, Gm, Gd, Gh)
                Ky, Km, Kd, Kh = GMT2Khour(Gy1, Gm1, Gd1, Gh1)
                if Km<5:
                    cnt = cnt+1
                    continue
                elif Km==5 and Kd<8:
                    cnt = cnt+1
                    continue
                time = str(Ky)+"-"+str(Km).zfill(2)+"-"+str(Kd).zfill(2)+" "+str(int(Kh))+":00"
                #print(time)
                
                while(dscnt<len(ds)):
                    
                    if ds["time"][dscnt] == time:
                        ds[plant_id+"_"+str(num)][dscnt] = float(dataset.iloc[cnt,[3]])
                        #print(cnt)
    
                        break
                    else :
                        dscnt= dscnt+1
                cnt = cnt+1
            else:
                
                if len(dataset.iloc[cnt,[0]][0])>8:
                    Start = dataset.iloc[cnt,[0]][0]
                    Gy = int(Start[-9:-5])
                    Gm =  int(Start[-5:-3])
                    Sd = int(Start[-3:-1])-1
                    cnt= cnt+1
                    det = True
                    continue
                else:
                    if det or not(dataset.iloc[cnt,[1]][0]==dataset.iloc[cnt-1,[1]][0]):
    
                        Gd = Sd + int(dataset.iloc[cnt,[0]][0])
                        Gh = dataset.iloc[cnt,[1]][0]/100+dataset.iloc[cnt,[2]][0]
                        Gy1, Gm1 ,Gd1, Gh1 = Nextday(Gy, Gm, Gd, Gh)
                        
                        Ky, Km, Kd, Kh = GMT2Khour(Gy1, Gm1, Gd1, Gh1)
                        
                        
                        if Km<5:
                            cnt = cnt+1
                            continue
                        elif Km==5 and Kd<8:
                            cnt = cnt+1
                            continue
                        time = str(Ky)+"-"+str(Km).zfill(2)+"-"+str(Kd).zfill(2)+" "+str(int(Kh))+":00"
                       # print(time)
    
                        while(dscnt<len(ds)):
    
                            if ds["time"][dscnt] == time:
                                ds[plant_id+"_"+str(num)][dscnt] = float(dataset.iloc[cnt,[3]])
                              #  print(cnt)
                                break
                            else :
                                dscnt= dscnt+1
                        det = False
                    cnt = cnt+1
                
    
            
    
    
    ds.to_csv(path_of_weather+"weather_data_new_pred.csv",index = False, mode='w')
    ds.head(30)


# In[ ]:




