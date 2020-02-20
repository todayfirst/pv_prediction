# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 17:17:21 2019

@author: todayfirst
"""
import numpy as np

def run(Ptraining_data,training_data,coms_training_data, coms_P_data,test_mode):
    Pindex = list(Ptraining_data["coms_index"].astype(int))
    Tindex = list(training_data["coms_index"].astype(int))
    coms_training_data = np.asarray(coms_training_data)
    if test_mode[0] == 4:

        coms_P_data = coms_training_data[Pindex]

    coms_training_data = coms_training_data[Tindex]
    
    if test_mode[0] == 1:
        coms_P_data = np.asarray(coms_P_data)
        coms_P_data = coms_P_data[Pindex]
    
    return (coms_training_data, coms_P_data)
