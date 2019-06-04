# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 17:16:14 2019

@author: emsud
"""

import Pharse
import GetUrl
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from setting import Dir_name,Save_PATH,Data_PATH
from Cleanning import cleanText

def remove():
    node = pd.read_csv(Data_PATH+"node.csv",header=None)
    recom = pd.read_csv(Data_PATH+"recommend.csv",header=None)
    recom = recom.fillna(0)
    recom = recom.astype(int)
    recom = recom.astype(object)
    
    r_recom = np.array(recom)
    r_node = np.array(node)
    arr = np.zeros([len(recom),24],dtype=object)
    
    for i in range(len(recom)):
        print(i)
        cnt = 0
        for j in range(len(r_recom[i])):
            for k in range(len(r_node)):
                if r_recom[i][j] == r_node[k] :
                    arr[i][cnt] = r_recom[i][j]
                    cnt += 1
                    break
    tmp = pd.DataFrame(arr)
    tmp.to_csv(Data_PATH+"remove.csv",index=False,header=None)
    
    
    return arr


if __name__=="__main__":
    column=["Node","Title","Autor","Location","Description","Sellnum"]
    url_list=[]
    error=[]
    title=[]
    autor=[]
    descrip=[]
    sellnum=[]
    location=[]
    recomdlist=[]
    node=[]
    cnt=0
    os.makedirs("../"+Dir_name,exist_ok=True)
    url_list=GetUrl.saveUrl(1,2)
    
    for i in range(len(url_list)):
        try:
            data=Pharse.PharseData(url_list[i])
            cnt+=1##현재 상황 체크
            print(cnt)
            recomd_list=data.get_recommend_bookList()
            if recomd_list==-1:
                continue
            ID=list(recomd_list.keys())
            Recomdlist=cleanText(str(ID))
            Node=url_list[i].split('/')[-1]
            Title=data.get_Title()
            Autor=data.get_Autor()
            Des=data.get_Description()
            Sellnum=data.get_Sellnum()
            Location=cleanText(str(data.get_Location()))
        except:
            error.append(Node)
            continue
        recomdlist.append(Recomdlist)
        node.append(Node)
        title.append(Title)
        autor.append(Autor)
        if Des==-1:
            descrip.append(0)
        else:
            descrip.append(cleanText(Des))
        sellnum.append(Sellnum)
        location.append(Location)
        
    GetUrl.savefile("title.csv",title,'\n')
    GetUrl.savefile("autor.csv",autor,'\n')
    GetUrl.savefile("descrip.csv",descrip,'\n')
    GetUrl.savefile("sellnum.csv",sellnum,'\n')
    GetUrl.savefile("location.csv",location,'\n')
    GetUrl.savefile("node.csv",node,'\n')
    GetUrl.savefile("recommend.csv",recomdlist,'\n')
    
    df=pd.DataFrame(columns=column)
    df["Node"]=node
    df["Title"]=title
    df["Autor"]=autor
    df["Location"]=location
    df["Sellnum"]=sellnum
    df["Description"]=descrip
    
    
    tmp=remove()
    
    
    df.to_csv(Save_PATH+"data.csv",encoding='cp949',index=False)
    
    

