# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:08:17 2019

@author: emsud
"""

import re
from konlpy.tag import Kkma

kkma=Kkma()

def get_Keyword(description):
    words = kkma.nouns(description)
    return words


def cleanText(readData):
    #텍스트에 포함되어 있는 특수 문자 제거
    cleanr = re.compile('<.*?>')
    cleanr2 = re.compile('[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9 , ]') 
    text = re.sub(cleanr, '', readData)
    text = re.sub(cleanr2,'',text)
    return text

