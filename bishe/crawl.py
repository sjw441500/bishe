# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def getKoubei(html):
    tmplst=[]
    #tmpmark=[]
    soup=BeautifulSoup(html,'html.parser')
    lst=soup.find_all('p',class_='p1')
    mark=soup.find_all('p',class_='p2')
    
    for txt in lst:
        index=lst.index(txt)
        comDict={'comment':txt.text,'mark':int(mark[index].text)}
        tmplst.append(comDict)
    return tmplst
def getCommentUrl(comment_url):
    r=requests.get(comment_url)
    soup=BeautifulSoup(r.text,'html.parser')
    comment_list=soup.find_all('a',text="查看更多>>")
    print comment_list
    page_next=soup.find_all('a',text="下一页")
    print page_next
    #print len(page_next)
    if not len(page_next):
        #print temp_list
        #print type(temp_list)
        #return temp_list
        return
    else:
        isNext=page_next[0]['href']
        print isNext
        for x in comment_list:
            yield x['href']
            #temp_list.append(x['href'])
        #print temp_list
        #print('this is the page '+str(counter))
        #counter+=1
        getCommentUrl(isNext)
        

def getComment(url):
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')
    return soup.find_all("div",class_="article-contents")[0].text
    


base_url='http://car.bitauto.com'
r=requests.get('http://car.bitauto.com/xinaodia6l/')
#sprint type(r.text)
soup=BeautifulSoup(r.text,'html.parser')
more=soup.find_all('a',text="查看更多口碑")[0]['href']
comment_url=base_url+more
#print comment_url
koubei=str(soup.find_all('div',class_='txt-box kb-card')[0])
soup2=BeautifulSoup(koubei,'html.parser')
good=str(soup2.find_all('li')[0])
bad=str(soup2.find_all('li')[1])
goodComment=getKoubei(good)
badComment=getKoubei(bad)
all_comment_url=getCommentUrl(comment_url)
#print type(all_comment_url)
#print all_comment_url
all_comment=[]
for comment in all_comment_url:
    #print comment
    tmp=getComment(comment)
    all_comment.append(tmp)
save_file=open('cars.txt','a')
save_file.writelines(str(all_comment))

    
    
    











        
