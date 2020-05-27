import requests
import bs4
import re

url = "https://old.reddit.com/r/acturnips/new"
headers = {'User-Agent': 'Mozilla/5.0'}
swRegex = re.compile(r'\d{4}-\d{4}-\d{4}')
priceRegex = re.compile(r'\d{3}')
userRegex = re.compile(r'ago by (.*?)')
#test=userRegex.findall('ago by penismanawesomedued by the way the price is 500 Bells')
#print(test[0])
tListings = []


def methodName(link,listings):
    curPost=requests.get(link,headers=headers)
    curPageHtml=bs4.BeautifulSoup(curPost.text,'html.parser')
    #print(curPageHtml.text)
    words=curPageHtml.find("div",class_="thing")
    cleanPost=words.text.strip('•comentsharvidport 1234567890')
    FC=swRegex.findall(cleanPost)
    
    
    
    #price=priceRegex.search()
    #print(price)


    if cleanPost[:6]=='Active':
        #print('awesome')
        if len(FC)>0:
            FC=FC[0]
           # print('Friend Code is SW-'+FC)
            
            cleanPost=cleanPost.replace(FC,'')
            price=priceRegex.findall(cleanPost)
        else:
            FC=''
        if len(price)>0:
            price=price[0]
           # print('Price is '+price+' Bells')
        else:
            price=''
           # print('I dont know the price lol')
        curListing = {
                        "price" : price,
                        "FC" : "SW-"+FC,
                        "url" : link
                    }
        listings.append(curListing)
    


# Headers to mimic a browser visit


# Returns a requests.models.Response object
for i in range(3):
    res = requests.get(url, headers=headers)

    try:
        res.raise_for_status()
    except:
        print("Error accessing turnip prices")
    
    #print(res)    
    pageHtml=bs4.BeautifulSoup(res.text,'html.parser')
    elems = pageHtml.find_all("a", class_="title may-blank")
    
    url=pageHtml.find("span",class_="next-button").find("a" , recursive=False)['href'] 
    print(url)
    

    #print(elems[0].text)
    #print(elems[0]['href'])
    #print('https://old.reddit.com'+elems[0]['href'])

    for j in range(len(elems)):
    # print('https://old.reddit.com'+elems[i]['href'])
    #  methodName("https://old.reddit.com"+elems[i]['href'],tListings)
        try:
            methodName("https://old.reddit.com"+elems[j]['href'],tListings)
        except:
            pass

  
print(tListings)