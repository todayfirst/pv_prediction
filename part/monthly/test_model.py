# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:52:43 2019

@author: todayfirst
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
'''
path = "E:\\skt\\코드정리_중간발표\\result\\cnn\\0~8\\6\\"

df = pd.read_csv(path+"6_yy_Result.csv")

test_labels1 = []
test_predictions1 =[]
test_1daypredict = []
for i in range(len(df)):
    if np.isnan(df["predict"][i]):
        continue
    else:
        test_labels1.append(float(df["0h"][i]))
        test_predictions1.append(float(df["Med_predict"][i]))
       # test_1daypredict.append(float(df["jp_SKT"][i]))
test_labels1 = np.asarray(test_labels1)
test_predictions1 = np.asarray(test_predictions1)
test_1daypredict = np.asarray(test_1daypredict)

from scipy.stats import gaussian_kde

xy = np.vstack([test_labels1,test_predictions1])
z = gaussian_kde(xy)(xy)

idx = z.argsort()
x, y, z = test_labels1[idx], test_predictions1[idx], z[idx]
plt.scatter(x, y, c=z, s=30, edgecolor='')

plt.xlabel('True Values [pv+2h]')
plt.ylabel('Predictions [pv+2h]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,1500])
plt.ylim([0,1500])
_ = plt.plot([-100, 5000], [-100, 5000])
fig = plt.gcf() #변경한 곳
plt.show()
fig.savefig(path+"_plot.png")
fig.clear()
del fig
plt.close

xy = np.vstack([test_labels1,test_1daypredict])
z = gaussian_kde(xy)(xy)

idx = z.argsort()
x, y, z = test_labels1[idx], test_1daypredict[idx], z[idx]
plt.scatter(x, y, c=z, s=30, edgecolor='')

plt.xlabel('True Values [pv+1 day]')
plt.ylabel('Predictions [pv+1 day]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,900])
plt.ylim([0,900])
_ = plt.plot([-100, 5000], [-100, 5000])
fig = plt.gcf() #변경한 곳
plt.show()
fig.savefig(path+"1day_plot.png")
fig.clear()
del fig
plt.close

'''



def run(ex_case, case, model,history, test_dataset, test_labels,forevalmax, forevalmin, cap,site_n):
    
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    
    
    plt.figure(figsize=(12,8))
    
    
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [pv+2h]')
    plt.plot(hist['epoch'], hist['mean_absolute_error'],
               label='Train Error')
    plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
               label = 'Val Error')
    plt.ylim([0,0.5])
    plt.legend()
    fig = plt.gcf()
    plt.show()
    
    dirname = "./result"+"//t"+str(site_n)+"//"+str(case)
    if not os.path.isdir(dirname): 
        os.mkdir(dirname)
    fig.savefig(dirname+"//"+str(ex_case)+"_history.png")
    fig.clear()
    
    del fig
    plt.close()
    
    
    test_predictions = model.predict(test_dataset).flatten()
    array_test_labels=pd.Series(test_labels).values
    array_test_predictions=pd.Series(test_predictions).values
    
    


    test_labels1 =(forevalmax-forevalmin)*test_labels+forevalmin
    test_predictions1 = (forevalmax-forevalmin)* test_predictions+forevalmin
    
    from scipy.stats import gaussian_kde
    
    xy = np.vstack([test_labels1,test_predictions1])
    z = gaussian_kde(xy)(xy)
    
    idx = z.argsort()
    x, y, z = test_labels1[idx], test_predictions1[idx], z[idx]
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
    fig.savefig(dirname+"//"+str(ex_case)+"_plot.png")
    fig.clear()
    del fig
    plt.close



    return (np.fabs(array_test_labels*(forevalmax - forevalmin) - array_test_predictions*(forevalmax - forevalmin))/( cap   )  ).mean(), test_predictions1,test_labels1
