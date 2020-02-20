# -*- coding: utf-8 -*-
import os
import config
from part import make_blank
from part import import_data
from part import import_coms
from part import make_multitemporal_data
from part import make_multitemporal_coms
from part import erase_skip_and_time
from part import erase_coms
from part import min_max_0to1
from part import make_name
from part import set_train_data
from part import set_train_coms
from part import mlp_model
from part import cnn_model
from part import combine_model
from part import fit_model

from part import test_model
from part import write_evaluation_result
import itertools
import pickle
import pandas as pd
import numpy as np

import pvlib



#%%

# all_case_number : 실험 조건 개수 - config.py 에서 설정한 개수
# site_n : 실험 지역 개수
# case : 현재 루프의 실험번호
# each_case : 현재 루프의 실험번호의 조건들 리스트
# plant_id : 실험 지역 id
# cap : 해당 실험 지역의 발전용량
# weather_ele : 날씨 정보 요소
# comsset : 사용하는 영상의 종류
# cnn_mode : cnn을 사용하는지 안하는지
# hours : 예측에 사용될 자료의 시간대
# no_coms : 위성영상 사용하지 않으려면 1, 사용하면 0
# patch_size : cnn 시 사용할 패치의 개수
# layers : cnn 시 레이어 정보
# combine_layers : cnn 시 레이어 정보
# numofex : 한 조건당 반복실험 횟수
# test_mode : 어떤 방식으로 테스트 할지
# NMAE : nMAE를 계산할 오차들을 저장함
# sum_nmae : 절대오차들의 합을 계산
# minute : 분단위의 영상을 위한 변수

all_case_number = len(config.all_case)

## case = 0
##each_case = config.all_case[0]
## site_n = 1
for site_n in range(1,7):
    NMAE = pd.DataFrame()
    new_NMAE = pd.DataFrame()
    for case, each_case in enumerate(config.all_case):
        (plant_id, cap, weather_ele, comsset, cnn_mode, hours, no_coms, patch_size, layers, combine_layers, numofex, test_mode )=config.iterate(case,site_n)
        #iter_weather = list(itertools.product(range(2), repeat = 9))
        
        #for iter_in in range(len(iter_weather)):
        
        #    weather_ele = []
        #    for in_weather in range(1,10):
        #        if iter_weather[iter_in][in_weather-1] == 1:
        #            weather_ele.append(in_weather)
            
        minute = [0]
        NMAE[str(case)] = np.zeros((100))
        sum_nmae = 0
        
        if cnn_mode==1:
            (zero_time_image, Pzero_time_image) = make_blank.run(comsset, minute, test_mode)
            (zero_time_image, Pzero_time_image) = import_coms.run(zero_time_image, Pzero_time_image, test_mode, comsset, plant_id, minute)
        
        basic_data, Pbasic_data = import_data.run(test_mode, comsset, plant_id, minute, weather_ele)
        
        training_data, Ptraining_data = make_multitemporal_data.run(basic_data, Pbasic_data, test_mode, comsset,hours, minute, weather_ele, plant_id)
        
        if cnn_mode==1:
            coms_training_data, coms_P_data = make_multitemporal_coms.run(zero_time_image, Pzero_time_image,patch_size, comsset, hours, minute, test_mode, len(basic_data),len(Pbasic_data))
    
        training_data, Ptraining_data = erase_skip_and_time.run(training_data, Ptraining_data,cnn_mode, test_mode, cap, comsset, hours, minute,6, 20 )
    
        if cnn_mode==1:
            coms_training_data, coms_P_data = erase_coms.run(Ptraining_data,training_data,
                                                             coms_training_data, coms_P_data,test_mode)
        
            print(str(len(training_data))+" : "+str(len(coms_training_data)))
            print(str(len(Ptraining_data))+" : "+str(len(coms_P_data)))
    
        if test_mode[0]==1 or test_mode[0] == 4:
            Pindex = Ptraining_data.pop("coms_index")
        training_data.pop("coms_index")  
    
        if not os.path.isdir("./result"+"//t"+str(site_n)+"//"+str(case)):
            if not os.path.isdir("./result"+"//t"+str(site_n)):
                os.mkdir("./result"+"//t"+str(site_n))
            os.mkdir("./result"+"//t"+str(site_n)+"//"+str(case))
        training_data.to_csv("./result"+"//t"+str(site_n)+"//"+str(case)+"//"+plant_id+"_Trainingdata.csv", mode='w')
       
        training_data, Ptraining_data,forevalmax, forevalmin,scaled_features,min_save, max_save = min_max_0to1.run(training_data, Ptraining_data, test_mode )
        
        training_data.to_csv("./result"+"//t"+str(site_n)+"//"+str(case)+"//"+plant_id+"_Trainingdata_min_max.csv", mode='w')

        with open("./result"+"//t"+str(site_n)+"//"+str(case)+"//"+plant_id+"_min.pickle", 'wb') as handle:
            pickle.dump(min_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open("./result"+"//t"+str(site_n)+"//"+str(case)+"//"+plant_id+"_max.pickle", 'wb') as handle:
            pickle.dump(max_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #with open('filename.pickle', 'rb') as handle:
      #      unserialized_data = pickle.load(handle)
      
        for_name = make_name.run(cnn_mode, no_coms, comsset, weather_ele, hours)
    
# ex_case = 0
        for ex_case in range(numofex):
            from tensorflow.keras import backend as K
            K.clear_session()

            if cnn_mode ==1:
                if ex_case==0:
                    train_dataset, test_dataset, train_labels, test_labels, for_name1 = set_train_coms.make_for_cnn(coms_training_data, coms_P_data, test_mode, training_data, Ptraining_data,hours,minute,comsset,cnn_mode,ex_case,for_name)
                else:
                    train_dataset, test_dataset, train_labels, test_labels = set_train_coms.make_for_cnn(coms_training_data, coms_P_data, test_mode, training_data, Ptraining_data,hours,minute,comsset,cnn_mode,ex_case,for_name)
            else : 
                if ex_case==0:
                    train_dataset, test_dataset, train_labels, test_labels, for_name1,var_list = set_train_data.make_for_mlp(test_mode, training_data, Ptraining_data,hours,minute,comsset,cnn_mode,ex_case,for_name)
                    with open("./result"+"//t"+str(site_n)+"//"+str(case)+"//"+plant_id+"_var_list.pickle", 'wb') as handle:
                        pickle.dump(var_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

                else:
                    train_dataset, test_dataset, train_labels, test_labels= set_train_data.make_for_mlp(test_mode, training_data, Ptraining_data,hours,minute,comsset,cnn_mode,ex_case,for_name)
            #if 'A' in df.columns:
            
            if cnn_mode ==1:
                model_cnn = cnn_model.create_cnn(np.shape(train_dataset[1])[1],np.shape(train_dataset[1])[2],
                                 np.shape(train_dataset[1])[3], layers,  ex_case)
                model_mlp = mlp_model.create_mlp(np.shape(train_dataset[0])[1],[], False)
                
                model=(combine_model.run(model_mlp, model_cnn, combine_layers))       
            else:
                model=(mlp_model.create_mlp(train_dataset.shape[1],layers, True))
    
                
            history = fit_model.run(model, train_dataset, train_labels,case,ex_case,50, 0.2,site_n)
            
            #print(test_model.run(ex_case, case, model,history, test_dataset, test_labels,forevalmax, forevalmin, cap))
            #NMAE[str(case)][ex_case],test_predictions,test_labels = test_model.run(ex_case, case, model,history, test_dataset, test_labels,forevalmax, forevalmin, cap,site_n)
            #print(NMAE[str(case)][ex_case])
            '''   del model
            if cnn_mode ==1:
                del model_cnn
                del model_mlp
            for i in range(10):
                gc.collect()'''

            #sum_nmae = sum_nmae+NMAE[str(case)][ex_case]
            #if(ex_case>4 and sum_nmae>0.065*(ex_case+1)):
           #     iseval = False
          #      break
          #  else:
         #       iseval = True
          #  
        #if iseval:
         #   write_evaluation_result.run(plant_id,Pindex,test_dataset,cap,test_labels,case,numofex,forevalmax, forevalmin,test_mode,NMAE,site_n)
        #NMAE.to_csv("./result"+"//t"+str(site_n)+"//"+str(case)+"//"+plant_id+"_Result.csv", mode='w')
      #  new_NMAE[str(iter_in)] = NMAE[str(case)]
      #  new_NMAE.to_csv("./result"+"//t"+str(site_n+iter_in)+"_weather_Result.csv", mode='w')
      #  break
   # new_NMAE.to_csv("./result"+"//t"+str(site_n)+"_weather_Result.csv", mode='w')