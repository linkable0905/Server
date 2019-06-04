# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 19:40:26 2019
@author: emsud
"""

import GetUrl
import re

class PharseData:
    def __init__(self,url):
        self.page=GetUrl.get_book_page(url)
        self.url=url
        
    def get_recommend_bookList(self):
        recommend_book_list={}
        if self.page != []:
            try:
                divfirst=self.page.findAll('div',attrs={'id':'divFirst'})
                recommend_book_area=divfirst[0].findAll('li')
            except:
                print(self.url)
            for i in range(len(recommend_book_area)):
                recommend_book_list[(recommend_book_area[i].get('data-goods-no'))]=recommend_book_area[i].find('p',attrs={"class":"goods_name"}).text
            return recommend_book_list
        else:
            return -1
    
    
    def get_Title(self):
        if self.page==[]:
            return -1
        else:
            return self.page.find('h2',attrs={"class":"gd_name"}).text
        
    def get_Autor(self):
        if self.page==[]:
            return -1
        else:
            try:
                athor = self.page.find('span',{"class":"gd_auth"}).text.strip()
            except:
                athor = self.page.find('span',{"class":"gd_pub"}).text.strip()
            return athor
        
    def get_Description(self):
        if self.page==[]:
            return -1
        else:
            try:
                des=des=self.page.find("textarea",{"class":"txtContentText"}).text
            except:
                return -1
            return des
    def get_Sellnum(self):
        if self.page==[]:
            return -1
        else:
            p=re.compile('[\d]*[\d]')
            m=p.search(self.page.find('span',{'class':'gd_sellNum'}).text)
            return m.group()
    def get_Location(self):
        loc=[]
        if self.page==[]:
            return -1
        else:
            location=self.page.findAll('a',{'class':'yLocaDepth'})
            for i in range(0,len(location)):
                loc.append(location[i].text.strip())
            return loc


