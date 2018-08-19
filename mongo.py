import pymongo
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import re

c = MongoClient()
db=c["mydatabase"]
article = db.articles

def insertIntoDB(date,title, content, source, url):
    post_Data ={'date': date, 'title':title,'content':content,'source':source,'url':url,'score':'NA'}
    """if(article.find({'title':title,'date':date,'source':source}).count()>0):
        print("already present")
    else:"""
    result = article.insert_one(post_Data)

def updateScore():
    article.find({'score':'NA'})
	
def getGoodNetworkNews():
    url = 'https://www.goodnewsnetwork.org/'
    html = requests.get(url)
    soup = BS(html.text)
    table = soup.find_all('h3',{'class':"entry-title td-module-title"})
    for i in table:
        k=i.find('a')['href']
        #print("url",k)
        browser = webdriver.PhantomJS(executable_path="D:/sw/phantomjs-2.1.1-windows/bin/phantomjs")
        browser.get(k)
        html = browser.page_source
        soup = BS(html, 'html.parser')
        time = soup.find('time')
        #print(time.string)
        try:
            title_article=soup.find('h1',{'class':"entry-title"})
            #print("TITLE",title_article.string)
            para = soup.find('div',{'class':'td-post-content'}).find_all('p')
            content=''
            for i in para:
                #if not(i.string is None):
                content=content+i.string
            insertIntoDB(time.string,title_article.string, content, "Good", content)
        except:
            print("removing video articles") #article
			
def newsFromGuardian():
    main_url = "https://newsapi.org/v2/everything?sources=the-guardian-uk&apiKey=fa6d77b861bc48c2a4bfd93ef6ceaeba"
    open_bbc_page = requests.get(main_url).json()
    article = open_bbc_page["articles"]
    browser = webdriver.PhantomJS(executable_path="D:/sw/phantomjs-2.1.1-windows/bin/phantomjs")
    try:
        for ar in article:
            print("TITLE:",ar["title"])
            browser.get(ar["url"])
            ans=''
            html = browser.page_source
            soup = BS(html, 'html.parser')
            table = soup.find('div',{'class':re.compile('content__article-body')}).find_all('p')
            for k in table:
                if k.string is not None:
                    ans=ans+k.string
            insertIntoDB(ar['publishedAt'],ar["title"], ans, "the-guardian-uk", ar["url"])
    except:
        print("removing video articles") #article
    
  
def newsFromBBC():
    main_url = " https://newsapi.org/v2/everything?sources=bbc-news&apiKey=95465951cbf447369c10a005ded49a0b"
    open_bbc_page = requests.get(main_url).json()
    article = open_bbc_page["articles"]
    results = []
    links = []
    browser = webdriver.PhantomJS(executable_path="D:/sw/phantomjs-2.1.1-windows/bin/phantomjs")
    for ar in article:
        print("TITLE:",ar["title"])
        print("DATE:",ar['publishedAt'])
        try:
            browser.get(ar["url"])
            ans=''
            html = browser.page_source
            soup = BS(html, 'html.parser')
            table = soup.find_all('div',{'class':"story-body__inner"})[0].find_all('p',{'class':"aria-hidden"})
            for div in table:
                div.decompose()
                table=soup.find_all('div',{'class':"story-body__inner"})[0].find_all('p')
                for k in table:
                    #if k.string is not None:
                    ans=ans+k.string
            insertIntoDB(ar['publishedAt'],ar["title"], ans, "BBC", ar["url"])
        except:
            print("removing video articles")
		
			
def newsFromCNBC():
    main_url = "https://newsapi.org/v2/everything?sources=cnbc&apiKey=cb28b795dd1e469ebbc02ea19535898a"
    open_cnbc_page = requests.get(main_url).json()
    article = open_cnbc_page["articles"]
    browser = webdriver.PhantomJS(executable_path="D:/sw/phantomjs-2.1.1-windows/bin/phantomjs")
    for ar in article:
        browser.get(ar["url"])
        ans=''		
        html = browser.page_source
        soup = BS(html, 'html.parser')
        try:
            table = soup.find_all('div',{'class':'group-container'})[1].find_all('p')
            for k in table:
                if k.string is not None:
                    ans=ans+k.string
            insertIntoDB(ar['publishedAt'],ar["title"], ans, "CNBC", ar["url"])
        except:
            print("removing video articles")

			
newsFromBBC()	
#newsFromGuardian()
getGoodNetworkNews()
#newsFromCNBC()
