# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 22:49:25 2019

@author: emsud
"""
import numpy as np
from makeLink import makeLink

def convert(graph=makeLink()):
    AdjMatrix=np.zeros((len(graph),len(graph)))
    Node=list(graph.keys())
    idx=0
    jdx=0
    
    for i in Node:
        AdjMatrix[idx][idx]=1
        jdx=0
        book_inNode=graph[i]
        for j in Node:
            if j in book_inNode:
                AdjMatrix[idx][jdx]=1
                AdjMatrix[jdx][idx]=1
            jdx+=1
        idx+=1
    
    return AdjMatrix
