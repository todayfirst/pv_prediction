# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 20:46:56 2019

@author: todayfirst
"""
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import RMSprop
#lossfunc = 'mean_squared_error'
lossfunc = 'mean_absolute_error'
#opt = Adam(lr =0.001, beta_1 = 0.9, beta_2 = 0.999, epsilon = 1e-8, decay = 0.0)
#opt = RMSprop(0.001)



def create_mlp(dim, layers, regress):
    inputs = Input(shape=(dim,))

    for i, f in enumerate(layers):
        if f[0] == 'F':
            if i ==0:
                x = Dense(f[1])(inputs)
            else: 
                x = Dense(f[1])(x)
                
        if f[0] == 'R':
            if i ==0:
                x = Activation('relu')(inputs)
            else: 
                x = Activation('relu')(x)
                
        if f[0] == 'D':
            if i==0:
                x = Dropout(f[1])(inputs)
            else:
                x = Dropout(f[1])(x)

        if f[0] == 'B':
            if i==0:
                x = BatchNormalization()(inputs)
            else:
                x = BatchNormalization()(x)
    if len(layers)==0:
        x= inputs
    if regress:
        x = Dense(1)(x)
        x = Activation("linear")(x)
    model = None
    model = Model(inputs, x)
    
    if regress:

        model.compile(loss=lossfunc,
            optimizer=Adam(lr =0.001, beta_1 = 0.9, beta_2 = 0.999, epsilon = 1e-8, decay = 0.0),
            metrics=['mean_absolute_error', 'mean_squared_error'])

    return model