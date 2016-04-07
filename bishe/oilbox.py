# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import random
import requests
from bs4 import BeautifulSoup


def get_all_url():
    base_url='http://car.bitauto.com'
    browser = webdriver.Firefox() 
    r=requests.get('http://wuhan.bitauto.com/')
    #print r.text
    soup=BeautifulSoup(r.text,'html.parser')
    trees=soup.find_all("div",class_="cartabs_all")
    soup1=BeautifulSoup(str(trees),'html.parser')
    all_url=[]
    for x in soup1('a'):
        all_url.append(x['href'])
    print all_url
    f=open('car_url.txt','a')
    sub_url=[]
    for url in all_url:
        browser.get(url)
        while 1:
            time.sleep(10)
            html_doc=browser.page_source
            soup=BeautifulSoup(html_doc,'html.parser')
            content=soup.find_all("div",id="divContent")
            if content:
                cars=content[0]
            else:
                break
            for x in cars('li'):
                #print x 
                soup=BeautifulSoup(str(x),'html.parser')
                sub=soup.find_all('a')
                if sub:
                    print str(base_url+sub[0]['href'])
                    sub_url.append(base_url+sub[0]['href'])

            try:
                browser.find_element_by_class_name('next').click()
                html_doc=browser.page_source
            except Exception as e:
                break
    f.writelines(str(sub_url))

def get_oilbox():
    f=open('car_url.txt','r')
    ff=open('oilbox_data.txt','a')
    content=f.readlines()
    car_list=content[0].split(',')
    config_list=[]
    for car_url in car_list:
        tmp=car_url+'peizhi/'
        config_list.append(tmp)
    oilbox_dic=[]
    browser = webdriver.Firefox()
    for config in config_list:      
        browser.get(config)
        time.sleep(15)
        html_doc=browser.page_source
        soup=BeautifulSoup(html_doc,'html.parser')
        name_lst=soup.find_all('td',class_='pd0')
        number=soup.find_all(text='燃油箱容积')
        print config_list.index(config)
        numbers=[]
        for number1 in number:
            tmp=number1.find_parent("th").find_next_siblings('td')
            if tmp:
                for n in tmp:
                    #print n.text
                    numbers.append(n.text)
                break
        
        names=[]
        for name in name_lst:
            namestr=str(name)
            #print namestr
            soup=BeautifulSoup(namestr,'html.parser')
            if soup.find_all('a'):
                names.append(soup.find_all('a')[0].text)
        names=list(set(names))
        if u'\u53c2\u6570\u7ea0\u9519' in names:
            names.remove(u'\u53c2\u6570\u7ea0\u9519')    
        if len(names)==len(numbers):
            count=len(names)
            for m in xrange(count):
                ff.writelines(str({"car_name":names[m],"number":numbers[m]})+'\n')

                           
def
