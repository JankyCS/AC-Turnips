import requests
import bs4
import re
import flask
from flask import request, jsonify

swRegex = re.compile(r'\d{4}-\d{4}-\d{4}')
priceRegex = re.compile(r'\d{3}')
userRegex = re.compile(r'ago by (.*?)')

#return bs4 object
def getPage(url,headers):
    res = requests.get(url, headers=headers)
    try:
        res.raise_for_status()
    except:
        pass

    pageHtml=bs4.BeautifulSoup(res.text,'html.parser')
    return pageHtml

#check if previous scrape already contained the given listing
def alreadyHas(tListings,link):
    for k in tListings:
        if k["url"]==link:
            return True
    return False

#check if a listing is still active, or if it is finished
def checkActivity(link,headers):
    curPost=requests.get(link,headers=headers)
    curPageHtml=bs4.BeautifulSoup(curPost.text,'html.parser')
   
    words=curPageHtml.find("div",class_="thing")
    cleanPost=words.text.strip('•comentsharvidport 1234567890')

    return cleanPost[:6]=='Active'

#add listing to array if the listing is still active
def addListing(link,listings,headers):
    curPost=requests.get(link,headers=headers)
    curPageHtml=bs4.BeautifulSoup(curPost.text,'html.parser')
   
    words=curPageHtml.find("div",class_="thing")
    cleanPost=words.text.strip('•comentsharvidport 1234567890')
    FC=swRegex.findall(cleanPost)

    if checkActivity(link,headers):
        if len(FC)>0:
            FC=FC[0]
            cleanPost=cleanPost.replace(FC,'')
            price=priceRegex.findall(cleanPost)
        else:
            FC=''
        if len(price)>0:
            price=price[0]
        else:
            price=''
        curListing = {
                        "price" : price,
                        "FC" : "SW-"+FC,
                        "url" : link
                    }
        listings.append(curListing)
    else:
        pass
    

# Returns an array of dcitionaries - turnip listings
def getListings(old=[]):
    url = "https://old.reddit.com/r/acturnips/new"
    headers = {'User-Agent': 'Mozilla/5.0'}
    tListings = []
    prev=[]
    for i in range(1):
        pageHtml=getPage(url,headers)
        elems = pageHtml.find_all("a", class_="title may-blank")
        url=pageHtml.find("span",class_="next-button").find("a" , recursive=False)['href'] 
        for j in range(len(elems)):
            link="https://old.reddit.com"+elems[j]['href']
            if alreadyHas(old,link):
                break
            try:
                addListing(link,tListings,headers)
            except:
                pass
    for i in range(len(old)):
        if checkActivity(old[i]['url'],headers):
            prev.append(old[i])
    
    
    tListings=tListings+prev
    print (tListings)
    return tListings