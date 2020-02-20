#!/usr/bin/env python
# coding: utf-8

# In[8]:


from __future__ import absolute_import, division, print_function, unicode_literals
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import math as mt
import copy
from PIL import Image as pilimg
import pvlib

# In[9]:
plant_info = pd.read_csv("F:\\Downloads\\data\\data\\plant_info.csv",sep=",", header=0)

comsset = ["le1b_vi006_ko005lc_","le1b_nr013_ko020lc_", "le1b_sw038_ko020lc_", "le1b_ir105_ko020lc_", "le1b_ir112_ko020lc_","le1b_ir123_ko020lc_"]
#comsset = ["le1b_ir01", "le1b_ir02", "le1b_wv", "le1b_swir","le1b_vis","le2_ins"]
#crop_gk2a_ami_le1b_vi006_ko005lc_201907241400
#crop_gk2a_ami_le1b_nr013_ko020lc_201907241400
#crop_gk2a_ami_le1b_sw038_ko020lc_201907241400
#crop_gk2a_ami_le1b_ir105_ko020lc_201907241400
#crop_gk2a_ami_le1b_ir112_ko020lc_201907241400

## modify : 각각 pv 발전량 데이터, crop된 영상(발전소별 영상 쌓은것 저장할 공간) 경로 지정
for plant_n in range(1,7):
    plant_id = "t"+str(plant_n)
    path_of_pv= "F:\\Downloads\\data\\data\\PV_weather_data_new_check.csv"
    path_crop = "F:\\Downloads\\data\\Cropped\\"+plant_id+"\\crop_image"
    path_data = "F:\\\Downloads\\data\\Cropped\\t"+str(plant_n)
    dataset = pd.read_csv(path_of_pv,sep=",", header=0)
    lat = plant_info["lat"][plant_n-1]
    lon = plant_info["lon"][plant_n-1]
    ## modify : 어떤 영상을 쌓을지 결정
    minute = [0] 
    img_size = 121
    
    #

 #천리안 위성의 시간은 GMT고 발전량에 사용된 시간은 KST임. KST를 GMT로 바꿔주는 함수. 
 #입력값 Ky, Km, Kd, Kh : 각각 KST의 년도, 월, 일, 시간
 #출력값 Gy, Gm, Gd, Gh : 각각 GMT의 년도, 월, 일, 시간 
 
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
     
     #1. csv파일로 pv 발전량, 아지무스, 엘레베이션, 중심픽셀 값 저장
     ### 발전량 데이터 인덱스에 맞게 데이터 파싱###
     
     ## 아지무스, 엘레베이션 설정 
     
    dataset = pd.read_csv(path_of_pv,sep=",", header=0)
    dataset['year'] = dataset['time'].str[:4]
    
    dataset['month'] = dataset['time'].str[5:7]
    
    dataset['day'] = dataset['time'].str[8:10]
    
    dataset['Khour'] = dataset['time'].str[-5:-3]
    
    #dataset['10sum'] = np.zeros((len(dataset),1))
    
    
    #dataset["day_number"] = np.zeros((len(dataset),1))
    #dataset.head(10)
    dataset["elevation"] = np.zeros((len(dataset),1))
    dataset["elevation_0.2"] = np.zeros((len(dataset),1))
    dataset["elevation_0.4"] = np.zeros((len(dataset),1))
    
    dataset["azimuth"] =   np.zeros((len(dataset),1))
    dataset["azimuth_0.2"] =   np.zeros((len(dataset),1))
    dataset["azimuth_0.4"] =   np.zeros((len(dataset),1))
    
    dataset["ap_elevation"] = np.zeros((len(dataset),1))
    dataset["ap_elevation_0.2"] = np.zeros((len(dataset),1))
    dataset["ap_elevation_0.4"] = np.zeros((len(dataset),1))
     
    
     
    for i in range(len(dataset)):
         time_str = dataset["time"][i]
         time_ts_plus9 = pd.Timestamp(time_str) - pd.Timedelta(hours = 9)
         time_ts_plus9_str = time_ts_plus9.strftime("%Y-%m-%d %H:%M:%S")
         solar_df = pvlib.solarposition.get_solarposition(time_ts_plus9_str,lat,lon)
         
         dataset["elevation"][i] = solar_df["elevation"]
         dataset["ap_elevation"][i] = solar_df["apparent_elevation"]
         dataset["azimuth"][i] = solar_df["azimuth"]
         
         time_ts_plus9 = time_ts_plus9 + pd.Timedelta(minutes= 20)
         time_ts_plus9_str = time_ts_plus9.strftime("%Y-%m-%d %H:%M:%S")
         solar_df = pvlib.solarposition.get_solarposition(time_ts_plus9_str,lat,lon)
         
         dataset["elevation_0.2"][i] = solar_df["elevation"]
         dataset["ap_elevation_0.2"][i] = solar_df["apparent_elevation"]
         dataset["azimuth_0.2"][i] = solar_df["azimuth"]
         
         time_ts_plus9 = time_ts_plus9 + pd.Timedelta(minutes= 20)
         time_ts_plus9_str = time_ts_plus9.strftime("%Y-%m-%d %H:%M:%S")
         solar_df = pvlib.solarposition.get_solarposition(time_ts_plus9_str,lat,lon)
         
         dataset["elevation_0.4"][i] = solar_df["elevation"]
         dataset["ap_elevation_0.4"][i] = solar_df["apparent_elevation"]
         dataset["azimuth_0.4"][i] = solar_df["azimuth"]
        
     #print(dataset.shape)
     
    ''' for i in range(0,24):
     dn = 10
     for j in range(0,10):
         
         if np.isnan(dataset[plant_id][240+i-24*(j+1)]):
             dn = dn-1
         else:
             dataset['10sum'][240+i] = dataset['10sum'][240+i]+dataset[plant_id][240+i-24*(j+1)]
     dataset['10sum'][240+i] = dataset['10sum'][240+i]/dn

     for i in range(11*24,len(dataset)):
     dn = 10
     for j in range(0,10):
         
         if np.isnan(dataset[plant_id][i-24*(j+1)]):
             dn = dn-1
         else:
             dataset['10sum'][i] = dataset['10sum'][i]+dataset[plant_id][i-24*(j+1)]
     dataset['10sum'][i] = dataset['10sum'][i]/dn
     '''
     

    ###공간 만들기 ###
    coms_data=[]
        
    df = []
    for i in range(len(comsset)):
        for m in minute:
            dataset[comsset[i]+"."+str(m)] = np.zeros((len(dataset),1))
        
    
    cnt = 0
    for i in range(len(dataset)):
    
    #for i in range(3000,9000):
    
        [Gy, Gm, Gd, Gh] = Khour2GMT(dataset.year.astype('int')[i],dataset.month.astype('int')[i],
                                     dataset.day.astype('int')[i],dataset.Khour.astype('int')[i])
    
        sGy = str(Gy)
        sGm = str(Gm)
        sGd = str(Gd)
        sGh = str(Gh)
        if Gm<10:
            sGm = "0"+str(sGm)
        if Gd<10:
            sGd = "0" + str(sGd)
        if Gh<10:
            sGh = "0" + str(sGh)
        ##크롭된 천리안 영상
    
        path_name =path_crop+'\\'+sGy+'\\'+'M'+sGm+'\\'+'D'+sGd+'\\'
        #F:\Downloads\data\b1\t1\crop_image\2019\M07\D24
        
        
        if os.path.exists(path_name):
            os.chdir(path_name)
    
        else:
            ##영상이 없으면 skip
            ## modify : 영상이 없는 시간대 프린트 원하지 않으면 수정
            cnt=cnt+1
            if cnt%24==0:
                print("case1"+str((sGy)+sGm+sGd+sGh))
                
            for coms in (comsset):
                for m in minute:
                    dataset[coms+"."+str(m)][i] = "skip"
            continue
    
        year_i = sGy
        month_i = sGm
        day_i = sGd
        GMT_i = sGh
    
    
    
        for m in minute:
            file_name =[]
            bool_skip  =[]
            for comscnt in range(len(comsset)):
                if comsset[comscnt] == 'le1b_vi006':
                    file_name.append('crop_gk2a_ami_'+comsset[comscnt]+str(year_i)+str(month_i)+str(day_i)+str(GMT_i)+str(m).zfill(2)+'.tif')
    #crop_gk2a_ami_le1b_vi006_ko005lc_201907241400
    #crop_gk2a_ami_le1b_nr013_ko020lc_201907241400
    #crop_gk2a_ami_le1b_sw038_ko020lc_201907241400
    #crop_gk2a_ami_le1b_ir105_ko020lc_201907241400
    #crop_gk2a_ami_le1b_ir112_ko020lc_201907241400
    #    comsset = ["le1b_vi006_ko005lc_","le1b_nr013_ko020lc_", "le1b_sw038_ko020lc_", "le1b_ir105_ko020lc_", "le1b_ir112_ko020lc_"]
    
                else :
                    file_name.append('crop_gk2a_ami_'+comsset[comscnt]+str(year_i)+str(month_i)+str(day_i)+str(GMT_i)+str(m).zfill(2)+'.tif')
    
                if not os.path.exists(file_name[comscnt]):
                    bool_skip.append(False)
                else:
                    bool_skip.append(True)
            for comscnt in range(len(comsset)):
                if bool_skip[comscnt]:    
                    #if comsset[comscnt] == 'le2_ins':
                        #bdata = np.load(file_name[comscnt])
                        #dataset[comsset[comscnt]+"."+str(m)][i] = bdata[(img_size-1)/2,(img_size-1)/2]
                    #else:
                    bdata = pilimg.open(file_name[comscnt])
                    bdata = np.array(bdata);
                    dataset[comsset[comscnt]+"."+str(m)][i] = bdata[int((img_size-1)/2),int((img_size-1)/2)]
                else:
                 ##영상이 없으면 skip, 단 ins와 vis는 검사
    
                    if comsset[comscnt] == 'le1b_vis' or comsset[comscnt] == 'le1b_vis' :
                        det_bool = True
                        for comscnt2 in range(len(comsset)):
                            if comsset[comscnt2] == 'le1b_vis' or comsset[comscnt2] == 'le1b_vis':
                                continue
                            else:
                                if bool_skip[comscnt2]==False:
                                    det_bool = False
                                    break
                        if det_bool:
                            dataset[comsset[comscnt]+"."+str(m)][i] = 0;
    
                        else :
                            dataset[comsset[comscnt]+"."+str(m)][i] = 'skip';
                            cnt=cnt+1
                    ## modify : 영상이 없는 시간대 프린트 원하지 않으면 수정
                    else : 
                        cnt=cnt+1
                        dataset[comsset[comscnt]+"."+str(m)][i] = 'skip';
    
                    if cnt%24==0:
                        print("case2"+str(year_i)+str(month_i)+str(day_i)+str(GMT_i)+" : "+str(cnt))
    
                    continue


    #dataset = dataset[240:]
    
    #dataset = dataset.reset_index()
    #dataset.drop("index", axis = 1, inplace = True)
    
    dataset.head(10)
    
    print(dataset.tail(20) )
    print(cnt/24)
    

    ##파일로 저장
    ## modify : 파일명 바꿀수 있음
    dataset.rename(columns={plant_id: '0h'}, inplace=True)
    dataset.to_csv(path_data+"//"+plant_id+"_dataset_with_coms_pixel.csv",index = False, mode='w')



#%%

########################### CNN 시작##############################
    #2. 영상을 날짜별, 시간별로 numpy array로 스택쌓아놓고 저장

    cnt =0
    cntout = len(comsset)
    image_s = []
    for m in minute:
        image_s.append([])
    
    while(cnt<cntout):
        for i,m in enumerate(minute):
            image_s[i].append([])
    
        cnt= cnt+1
        
    
    cnt = 0
    cnt_test = 0
    for i in range(len(dataset)):
      #  cnt_test = cnt_test+1
       # if cnt_test==24:
       #     break
    #for i in range(3000,9000):
    
        [Gy, Gm, Gd, Gh] = Khour2GMT(dataset.year.astype('int')[i],dataset.month.astype('int')[i],
                                     dataset.day.astype('int')[i],dataset.Khour.astype('int')[i])
    
        sGy = str(Gy)
        sGm = str(Gm)
        sGd = str(Gd)
        sGh = str(Gh)
        if Gm<10:
            sGm = "0"+str(sGm)
        if Gd<10:
            sGd = "0" + str(sGd)
        if Gh<10:
            sGh = "0" + str(sGh)
        ##크롭된 천리안 영상
    
        path_name =path_crop+'\\'+sGy+'\\'+'M'+sGm+'\\'+'D'+sGd+'\\'
    
        
        
        if os.path.exists(path_name):
            os.chdir(path_name)
    
        else:
            ##영상이 없으면 skip
            cnt=cnt+1
            if cnt%1000==0:
                print(str(year_i)+str(month_i)+str(day_i)+str(GMT_i))
            comscnt = 0;
            
            while(comscnt<cntout):
                for m in range(len(minute)):
                    coms = comsset[comscnt]
                    image_s[m][comscnt].append(np.zeros((61,61)))
                comscnt = comscnt+1
            continue
        
        year_i = sGy
        month_i = sGm
        day_i = sGd
        GMT_i = sGh
        for m_i,m in enumerate(minute):
            file_name =[]
            bool_skip  =[]
            for comscnt in range(len(comsset)):
                if comsset[comscnt] == 'le2_ins':
                    file_name.append('crop_coms_mi_'+comsset[comscnt]+"_ko000ps_"+str(year_i)+str(month_i)+str(day_i)+str(GMT_i)+str(m).zfill(2)+'.png.npy')
                else:
                    file_name.append('crop_coms_mi_'+comsset[comscnt]+"_ko000ps_"+str(year_i)+str(month_i)+str(day_i)+str(GMT_i)+str(m).zfill(2)+'.png')
                if not os.path.exists(file_name[comscnt]):
                    bool_skip.append(False)
                else:
                    bool_skip.append(True)
            for comscnt in range(len(comsset)):
                if bool_skip[comscnt]:    
    
                    if comsset[comscnt]=="le2_ins":
                        bdata = np.load(file_name[comscnt])
                        image_s[m_i][comscnt].append(bdata[:,:])
    
                    else :
                        bdata = pilimg.open(file_name[comscnt])
                        bdata = np.array(bdata);
                        image_s[m_i][comscnt].append(bdata[:,:,0])
    
                else:
                    image_s[m_i][comscnt].append(np.zeros((61,61)))
    
    
    # In[31]:
    
    
    #print(np.shape(image_s[0][0]))
    #plt.imshow(image_s[0][1][10])
    #plt.colorbar()
    #plt.show()
    
    
    # In[32]:
    
    
    comscnt = 0
    while(comscnt<cntout):
        for i,m in enumerate(minute):
            np.save(path_crop+"\\"+plant_id+"_"+comsset[comscnt]+"_"+"dataset_with_coms_pixel_"+str(m), image_s[i][comscnt])
        comscnt = comscnt+1
    
    
    ##파일로 저장
