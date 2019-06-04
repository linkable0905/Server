# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:35:55 2019

@author: emsud
"""

import numpy as np
import pandas as pd


node = pd.read_csv("./data/node.csv")
recom = pd.read_csv("./data/recommend.csv")

tf = 0

r_recom = np.array(recom)
r_node = np.array(node)
arr = np.zeros([len(recom),25])

for i in range(len(recom)):
    if i%100 == 0:
        print(i)
    cnt = 0
    for j in range(len(r_recom[i])):
        for k in range(len(r_node)):
            if cnt >=25 :
                print("?!")
                break
            if r_recom[i][j] == r_node[k] :
                arr[i][cnt] = r_recom[i][j]
                cnt += 1
                break

            


df = pd.DataFrame(arr)
df.to_csv("./remove.csv")