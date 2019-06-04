# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 23:31:36 2019

@author: emsud
"""

import numpy as np
import os
import sys

INF=6
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from setting import Data_PATH
link_table=[]

w=0
AdjMatrix=a.copy()
length=len(AdjMatrix)

for i in range(length):
    for j in range(length):
        if AdjMatrix[i][j]==0:
            AdjMatrix[i][j]=INF
        if i==j:
            AdjMatrix[i][j]=0
    
for i in range(length):
    for j in range(length):
        print(j)
        for k in range(length):
            if(AdjMatrix[j][k]>AdjMatrix[j][i]+AdjMatrix[i][k]):
                AdjMatrix[j][k]=AdjMatrix[j][i]+AdjMatrix[i][k]

np.save(Data_PATH+"depth_table.npy",AdjMatrix)
    