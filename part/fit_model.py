# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 22:59:41 2019

@author: todayfirst
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow import keras


def run(model, train_dataset, train_labels,case,ex_case,early_p, val_split, site_n):

    class PrintDot(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs):
            if epoch % 50 == 0: print(str(epoch)+"\n")
            print('.', end='')
            
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=early_p)
    history=model.fit(train_dataset, train_labels, batch_size=16, epochs=200,
        validation_split =val_split,
        callbacks=[early_stop,PrintDot()],verbose=0)
    
    dirname = "./result"+"//t"+str(site_n)+"//"+str(case)
    if not os.path.isdir(dirname):
        if not os.path.isdir("./result"+"//t"+str(site_n)):
            os.mkdir("./result"+"//t"+str(site_n))
        os.mkdir(dirname)
    model.save(dirname+"//all_"+str(ex_case)+'_model.h5')
    
    model_json = model.to_json()
    if ex_case==0:
        with open(dirname+"//"+str(ex_case)+"model_structure.json", "w") as json_file : 
            json_file.write(model_json)
    model.save_weights(dirname+"//"+str(ex_case)+"_model_weights.h5")
    
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
    
    fig.clear()
    
    del fig
    plt.close()
    
   # print(str(ex_case)+" --end-------------------------\n")
    return history
