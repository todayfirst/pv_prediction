# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 21:29:59 2019

@author: todayfirst
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def make_for_mlp(test_mode, training_data, Ptraining_data,hours,minute,comsset, cnn_mode,ex_case,for_name):

    if test_mode[0] == 1 or test_mode[0] == 4 :
        test_dataset = Ptraining_data[:]
        train_dataset = training_data[:]
    if test_mode[0] == 2:
        test_dataset.pop('test')
        train_dataset.pop('test')
    if test_mode[0] == 3:
        train_dataset = training_data[:]
        train_dataset.reset_index(inplace = True)
        train_dataset.drop("index", axis=1,inplace = True)

        split = train_test_split(train_dataset,  test_size=test_mode[1])
        (train_dataset, test_dataset) = split

    train_labels = train_dataset.pop('2h')
    test_labels = test_dataset.pop('2h')

    cntout = len(comsset)
    if cnn_mode==1:
        
        for i in hours:
            if not (i==0):
                comscnt = 0
                while(comscnt<cntout):
                    for m_i, m in enumerate(minute):
                        train_dataset.pop(comsset[comscnt]+"_"+str(i)+"."+str(m))
                        test_dataset.pop(comsset[comscnt]+"_"+str(i)+"."+str(m))
                    comscnt = comscnt+1
            if i==0:
                comscnt = 0
                while(comscnt<cntout):
                    for m_i, m in enumerate(minute):
                        train_dataset.pop(comsset[comscnt]+"."+str(m))
                        test_dataset.pop(comsset[comscnt]+"."+str(m))
                    comscnt = comscnt+1
                continue
                
    if ex_case==0:
        var_list = []
        num0ffeature=0
        for each in train_dataset:
            print(each)
            num0ffeature = num0ffeature+1
            var_list.append(each)
        for_name1 = for_name+"num of features__"+str(num0ffeature)+")"
        print("number of features : "+str(num0ffeature))
        print("test data #: "+str(len(test_dataset)))
        print("train data #: "+str(len(train_dataset)))


    train_dataset = np.asarray(train_dataset)
    test_dataset  = np.asarray(test_dataset)
    test_labels = np.asarray(test_labels)
    train_labels = np.asarray(train_labels)
    if ex_case==0:
        return train_dataset, test_dataset, train_labels, test_labels, for_name1, var_list
    else:
        return train_dataset, test_dataset, train_labels, test_labels