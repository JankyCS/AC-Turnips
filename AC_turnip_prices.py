import requests
import bs4
import re
import flask
from flask import request, jsonify

swRegex = re.compile(r'\d{4}-\d{4}-\d{4}')
priceRegex = re.compile(r'\d{3}')
userRegex = re.compile(r'ago by (.*?)')
#test=userRegex.findall('ago by penismanawesomedued by the way the price is 500 Bells')
#print(test[0])

def getPage(url,headers):
    res = requests.get(url, headers=headers)
    try:
        res.raise_for_status()
    except:
        print("Error accessing turnip prices")
    
    #print(res)    
    pageHtml=bs4.BeautifulSoup(res.text,'html.parser')
    return pageHtml

def alreadyHas(tListings,link):
    for k in tListings:
        if k["url"]==link:
            return True
    return False

def checkActivity(link,headers):
    curPost=requests.get(link,headers=headers)
    curPageHtml=bs4.BeautifulSoup(curPost.text,'html.parser')
   # print(curPageHtml.text)
    words=curPageHtml.find("div",class_="thing")
    cleanPost=words.text.strip('•comentsharvidport 1234567890')
    #print(cleanPost)
    return cleanPost[:6]=='Active'

def methodName(link,listings,headers):
    curPost=requests.get(link,headers=headers)
    curPageHtml=bs4.BeautifulSoup(curPost.text,'html.parser')
    #print(curPageHtml.text)
    words=curPageHtml.find("div",class_="thing")
    cleanPost=words.text.strip('•comentsharvidport 1234567890')
    FC=swRegex.findall(cleanPost)

    #print("here")
    if checkActivity(link,headers):
        
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
    else:
        pass
        #print("failed check")
    


# Headers to mimic a browser visit


# Returns a requests.models.Response object
def pogG(old=[]):
    url = "https://old.reddit.com/r/acturnips/new"
    headers = {'User-Agent': 'Mozilla/5.0'}
    tListings = []
    prev=[]
    for i in range(2):
        pageHtml=getPage(url,headers)
        elems = pageHtml.find_all("a", class_="title may-blank")
        
        url=pageHtml.find("span",class_="next-button").find("a" , recursive=False)['href'] 

        for j in range(len(elems)):
            link="https://old.reddit.com"+elems[j]['href']
           # print(link)
            if alreadyHas(old,link):
               # print("Bouta break")
                break
            try:
                methodName(link,tListings,headers)
            except:
                pass
    for i in range(len(old)):
        if checkActivity(old[i]['url'],headers):
            prev.append(old[i])
        #print (tListings)
    
    tListings=tListings+prev
    return tListings

#print(pogG([{'price': '', 'FC': 'SW-4772-6081-6233', 'url': 'https://old.reddit.com/r/acturnips/comments/grdjjq/sw_nooklings_buying_for_1_4_2/'}, {'price': '395', 'FC': 'SW-7354-5011-4151', 'url': 'https://old.reddit.com/r/acturnips/comments/grdigd/sw_raccoon_dog_children_buying_root_vegetables/'}, {'price': '530', 'FC': 'SW-7708-9296-9194', 'url': 'https://old.reddit.com/r/acturnips/comments/grdfd7/sw_capitalist_parasites_looking_to_exploit_the/'}, {'price': '', 'FC': 'SW-6670-5357-7995', 'url': 'https://old.reddit.com/r/acturnips/comments/grd5eg/sw_nooklings_want_vegetables_for_twofivtynine/'}, {'price': '286', 'FC': 'SW-7048-5965-4202', 'url': 'https://old.reddit.com/r/acturnips/comments/grczyb/sw_anyone_interested_at_286/'}, {'price': '', 'FC': 'SW-7065-1875-2996', 'url': 'https://old.reddit.com/r/acturnips/comments/grcsnj/swtimtom_serling_for_four_nine_nine/'}, {'price': '', 'FC': 'SW-7940-1887-0105', 'url': 'https://old.reddit.com/r/acturnips/comments/grcnft/sw_feral_rats_will_grab_your_nips_for/'}, {'price': '', 'FC': 'SW-0862-4195-1517', 'url': 'https://old.reddit.com/r/acturnips/comments/grcndu/sw_merry_and_pippin_buying_for_three_eight_seven/'}, {'price': '', 'FC': 'SW-2808-7836-0292', 'url': 'https://old.reddit.com/r/acturnips/comments/grc877/sw_rats_are_buying_for_two1three/'}, {'price': '440', 'FC': 'SW-0106-2469-5512', 'url': 'https://old.reddit.com/r/acturnips/comments/grc4ak/sw_boys_buying_at_forforoh/'}, {'price': '100', 'FC': 'SW-5354-8567-8790', 'url': 'https://old.reddit.com/r/acturnips/comments/grbze7/sw_selling_for_three_nine_oh/'}, {'price': '', 'FC': 'SW-0821-1342-1438', 'url': 'https://old.reddit.com/r/acturnips/comments/grbwpw/sw_looking_to_buy_turnips/'}]))