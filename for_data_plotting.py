#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 14:18:55 2020

@author: todayfirst

"""
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from celluloid1 import celluloid
fig, axes = plt.subplots(2)
camera = celluloid.Camera(fig)

pv_data1 = pd.read_csv(".//data//E2MS_9Site_PV_Power.csv")
pv_data1 = pv_data1["t1"]

pv_data2 = pd.read_csv(".//data//E2MS_9Site_PV_Power.csv")
pv_data2 = pv_data2["t2"]

t = np.linspace(0, 50,50, endpoint=False)
for_x = np.linspace(0, len(pv_data1) - len(t),len(pv_data1) - len(t), endpoint = False )


for i in range(len(for_x)):
    axes[0].plot(t, pv_data1.iloc[t+i], color = 'blue')
    axes[1].plot(t, pv_data2.iloc[t+i], color = 'blue')
    camera.snap()
animation = camera.animate(interval = 50, blit = True)

animation.save(
    "see_pv.gif",
    dpi=100

)
