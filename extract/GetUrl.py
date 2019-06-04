# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 21:45:22 2019

@author: emsud
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from setting import Driver_PATH,yes24_PATH,Save_PATH
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(Driver_PATH)
driver.implicitly_wait(3)
driver.get('https://www.yes24.com/Templates/FTLogin.aspx')
# 아이디/비밀번호를 입력해준다.
driver.find_element_by_name('SMemberID').send_keys('emsud')
driver.find_element_by_name('SMemberPassword').send_keys('dhslrtldk!1')
driver.find_element_by_xpath('//*[@type="button"]').click()


def get_book_page(id):
    try:
        driver.get(yes24_PATH+id)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'divFirst')))
    except Exception:
        print(id+" is no info")
        #return []

    html = driver.page_source
    page = BeautifulSoup(html,'html.parser')
        
    return page
    

def get_bestseller_page(url):
    urls=[]
    book_urls=[]
    driver.get('http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=06&PageNumber='+url+'&FetchSize=80')
    html = driver.page_source
    page = BeautifulSoup(html,'html.parser')
    
    books=page.findAll('td',{'class':'goodsTxtInfo'})
    for book in books:
        links = book.select('p > a')
        for link in links :
              if link.get('href') != -1:
                    urls.append(link.get('href'))
    i = 1
    while i < len(urls):
        if urls[i] == urls[i-1] :
             book_urls.append(urls[i])
             i=i+2
        else :
            i=i+1
    return book_urls


def saveUrl(start_page_num,end_page_num):
    list=[]
    for i in range (start_page_num,end_page_num,1):
        urls = get_bestseller_page(str(i))
        list+=urls
        
    return list
        

def savefile(filename,obj,d):
    output_file=Save_PATH+filename
    with open(output_file,'w',newline='') as f:
        writer=csv.writer(f,delimiter=d)
        writer.writerow(obj)
