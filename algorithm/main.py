# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 23:31:36 2019

@author: emsud
"""

import queue
import numpy as np
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from DictToAdj import convert
from setting import Data_PATH
link_table=[]

w=0
AdjMatrix=convert()
length=len(AdjMatrix)
for i in AdjMatrix:
    q=queue.Queue()
    print(w)
    visit=np.zeros(length)
    link=[[],[],[],[],[],[]]
    q.put(w)
    visit[w]=1
    w+=1
    qszie=q.qsize()
    depth=0
    cnt=0
    
    while(q.qsize()):
        cnt+=1
        current_node=q.get()
        link[depth].append(current_node)
        if cnt==qszie:
            depth+=1
            cnt=0
        for j in range(length):
            if(AdjMatrix[current_node][j]==1):
                if(visit[j]==0):
                    visit[j]=1
                    q.put(j)
        if cnt==0:
            qszie=q.qsize()
        if depth>=6:
            break
    link_table.append(link)
      
table=np.zeros([length,length],dtype=float)

for i in range(length):
    for j in range(1,len(link_table[i])):
        for k in link_table[i][j]:
            table[i][k]=j

array = table
sellnum = pd.read_csv(Data_PATH+"./sellnum.csv",header=None)
num = np.array(sellnum)

arr=np.zeros([len(num),len(num)])

for i in range(len(array)):
    print(i)
    for j in range(len(array)):
        n = array[i][j]
        if n == 0:
            arr[i][j] = 0
        else:
            arr[i][j] = np.sign(num[j]) * (np.abs(num[j])) ** (1 / n)

np.save(Data_PATH+"Table.npy",arr)
    
    