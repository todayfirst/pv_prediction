# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 22:22:20 2019

@author: todayfirst
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

def run(plant_id,Pindex,test_dataset,cap,test_labels,case,numofex,forevalmax, forevalmin,test_mode,NMAE,site_n):

    model_test =[]
    dirname = "./result"+"//t"+str(site_n)+"//"+str(case)
    weight = 0
    for i in range(numofex) :
        model_test.append(load_model(dirname+"//"+str(i)+'_model1.h5'))
        weight = weight + (1/NMAE[str(case)][i])*(1/NMAE[str(case)][i])
    
    test_predictions_aver = model_test[0].predict(test_dataset).flatten()*1/NMAE[str(case)][0]*(1/NMAE[str(case)][0]) / weight
    test_predictions_med = np.zeros((len(test_predictions_aver),numofex))
    
    for i in range(numofex):
        if i ==0:
            test_predictions_med[:,i] = model_test[i].predict(test_dataset).flatten()
            continue
        test_predictions_med[:,i] = model_test[i].predict(test_dataset).flatten()
        test_predictions_aver =test_predictions_aver +  test_predictions_med[:,i]*1/NMAE[str(case)][i]*(1/NMAE[str(case)][i]) / weight
        
    
    
    test_predictions_aver = (forevalmax-forevalmin)* test_predictions_aver+forevalmin
    test_predictions_med = (forevalmax-forevalmin)* test_predictions_med+forevalmin
    test_predictions_med = np.sort(test_predictions_med, axis = 1)
    test_predictions_med = test_predictions_med[:,int(numofex/2)]
    
    #test_labels = (forevalmax-forevalmin)* test_labels+forevalmin

    
    if test_mode[0]==1:
        writethis = pd.read_csv("./data//"+plant_id+"//"+plant_id+"_1_day_ahead_forecasting_result.csv",sep=",",header=0)
        nmae = 0
        nmae_1day = 0
        Med_nmae = 0
        
        writethis["error"] = np.nan
        writethis["error_1day"] = np.nan
        writethis["Med_error"] = np.nan
    
        
        writethis["true"] = np.nan
        writethis["predict"] = np.nan
        writethis["Med_predict"] = np.nan
        for i in range(len(Pindex)):
            
            index = int(Pindex.iloc[i])+242
            error = abs(writethis["0h"][index]-test_predictions_aver[i])
            Med_error = abs(writethis["0h"][index]-test_predictions_med[i])
            
            if plant_id == 'jp' or plant_id == 'ham':
                error_1day = abs(writethis["0h"][index]-writethis[plant_id+"_SKT"][index])
                writethis["error_1day"][index] = error_1day
                nmae_1day = nmae_1day + error_1day
            writethis["predict"][index] = test_predictions_aver[i]
            writethis["Med_predict"][index] = test_predictions_med[i]
            
            writethis["true"][index] =test_labels[i]
            writethis["error"][index] = error
            writethis["Med_error"][index] =  Med_error
    
    
            nmae = nmae + error
    
            Med_nmae = Med_nmae + Med_error
            
        writethis["NMAE"] = np.nan
        writethis["NMAE"][0] = nmae/len(Pindex)/cap
        
        print("2hour: "+ str(nmae/len(Pindex)/cap))
    
        writethis["Med_NMAE"] = np.nan
        writethis["Med_NMAE"][0] = Med_nmae/len(Pindex)/cap
        
        print("2hour: "+ str(Med_nmae/len(Pindex)/cap))
            
        
        
        writethis["NMAE_1day"] = np.nan
        writethis["NMAE_1day"][0] = nmae_1day/len(Pindex) /cap
        
        
        print("1day: "+ str(nmae_1day/len(Pindex)/cap))
        if plant_id=='ham' or plant_id == 'jp':
            writethis = writethis[['time', '0h', 'predict','error',"NMAE",'Med_predict','Med_error','Med_NMAE','true',plant_id+"_SKT","error_1day",'NMAE_1day']]
        else:
            writethis = writethis[['time', '0h', 'predict','error',"NMAE",'Med_predict','Med_error','Med_NMAE','true']]
        writethis.to_csv("./result"+"//"+str(case)+"//"+str(case)+"_"+plant_id+"_Result.csv", mode='w')

          
    from scipy.stats import gaussian_kde
    
    xy = np.vstack([test_labels,test_predictions_aver])
    z = gaussian_kde(xy)(xy)
    
    idx = z.argsort()
    x, y, z = test_labels[idx], test_predictions_aver[idx], z[idx]
    plt.scatter(x, y, c=z, s=30, edgecolor='')
    
    plt.xlabel('True Values [pv+2h]')
    plt.ylabel('Predictions [pv+2h]')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0,cap])
    plt.ylim([0,cap])
    _ = plt.plot([-100, 5000], [-100, 5000])
    fig = plt.gcf() #변경한 곳
    plt.show()
    fig.savefig("./result"+"//t"+str(site_n)+"//"+str(case)+"//"+str(case)+"_"+plant_id+"_plot_average.png")
    fig.clear()
    del fig
    plt.close
    print((np.fabs(test_labels - test_predictions_aver)/( cap   )  ).mean())
    NMAE[str(case)][numofex] = (np.fabs(test_labels - test_predictions_aver)/( cap   )  ).mean()
    
    
    xy = np.vstack([test_labels,test_predictions_med])
    z = gaussian_kde(xy)(xy)
    
    idx = z.argsort()
    x, y, z = test_labels[idx], test_predictions_med[idx], z[idx]
    plt.scatter(x, y, c=z, s=30, edgecolor='')
    
    plt.xlabel('True Values [pv+2h]')
    plt.ylabel('Predictions [pv+2h]')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0,cap])
    plt.ylim([0,cap])
    _ = plt.plot([-100, 5000], [-100, 5000])
    fig = plt.gcf() #변경한 곳
    plt.show()
    fig.savefig("./result"+"//t"+str(site_n)+"//"+str(case)+"//"+str(case)+"_"+plant_id+"_plot_med.png")
    fig.clear()
    del fig
    plt.close
    print((np.fabs(test_labels - test_predictions_med)/( cap   )  ).mean())
    NMAE[str(case)][numofex+1] = (np.fabs(test_labels - test_predictions_med)/( cap   )  ).mean()