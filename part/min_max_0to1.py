# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 17:43:53 2019

@author: todayfirst
"""
import math as mt
def run(training_data, Ptraining_data, test_mode ):
    scaled_features = {}
    min_save = {}
    max_save = {}
    for each in training_data:
        if each == "test":
            continue

        #print(each)
        maxx1, minn1 = training_data[each].max(), training_data[each].min()
        if test_mode[0] ==1 or test_mode[0] ==4:
            
            maxx2, minn2 = Ptraining_data[each].max(),Ptraining_data[each].min()
            if mt.isnan(maxx2) :
                maxx = maxx1
            else:
                if maxx1>maxx2:
                    maxx = maxx1
                else:
                    maxx = maxx2
                
            if  mt.isnan(minn2):
                minn = minn1
            else:
                if minn1<minn2:
                    minn = minn1
                else:
                    minn = minn2
        else:
            maxx = maxx1
            minn = minn1
        
        scaled_features[each] = [maxx, minn]
        training_data.loc[:, each] = (training_data[each] - minn)/(maxx-minn)
        if test_mode[0] ==1 or test_mode[0] ==4:
            
            Ptraining_data.loc[:, each] = (Ptraining_data[each] - minn)/(maxx-minn)
        
        if each == "2h":
            forevalmax = maxx
            forevalmin = minn
        min_save[each] = minn
        max_save[each] = maxx
    return (training_data, Ptraining_data,forevalmax, forevalmin,scaled_features,min_save,max_save )