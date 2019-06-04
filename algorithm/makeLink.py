# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 18:00:00 2019

@author: emsud
"""
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from setting import Data_PATH

def makeLink():
    graph={}
    with open(Data_PATH+"node.csv",'r',newline='') as f1:
        with open(Data_PATH+"remove.csv",'r',newline='') as f2:
            while True:
                node=f1.readline()
                node=node.strip('\n')
                node=node.strip()
                recommend=f2.readline()
                if not node and not recommend:
                    break
                recommend=recommend.strip('\n')
                recommend=recommend.strip()
                recommend=recommend.split(',')
                graph[node]=recommend
    
    return graph

def makeGraph():
    graph={}
    node=pd.read_csv(Data_PATH+"node.csv",header=None)
    link=pd.read_csv(Data_PATH+"remove.csv",header=None)
    length=len(node)
    for i in range(length):
        graph[(node[0].iloc[i])]=[]
    for i in range(length):
        for j in range(0,24):
            if link[j][i]!=0:
                u=node[0].iloc[i]
                v=link[j][i]
                graph[u].append(v)
                graph[v].append(u)
    
    return graph
        

            
        
        


        
