# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 23:31:36 2019

@author: emsud
"""

import queue
import makeLink
import numpy as np
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from DictToAdj import convert
from setting import Data_PATH
link_table=[]

graph=makeLink.makeLink()
key=list(graph.keys())
w=0
for i in key:
    q=queue.Queue()
    print(w)
    visit=np.zeros(len(key))
    link=[[],[],[],[],[],[]]
    q.put(i)
    visit[w]=1
    w+=1
    qszie=q.qsize()
    depth=0
    cnt=0
    
    while(q.qsize()):
        current_node=q.get()
        if current_node=='0':
            continue
        cnt+=1
        link[depth].append(current_node)
        if cnt==qszie:
            depth+=1
            cnt=0
        for j in graph[current_node]:
            if j=='0':
                continue
            if(visit[key.index(j)]==0):
                visit[key.index(j)]=1
                q.put(j)
        if cnt==0:
            qszie=q.qsize()
        if depth>=6:
            break
    link_table.append(link)
      
table=np.zeros((len(key),len(key)),dtype=float)
#
#for i in range(len(key)):
#    for j in range(1,len(link_table[i])):
#        for k in link_table[i][j]:
#            table[i][key.index(k)]=j
#
#np.save("./Table",table)
    
    