import json
import requests
from datetime import datetime
from billy.multiset import Multiset

#grab passwords from this file, hidden from github
execfile('settings.py')


def getInventory(steamid):
    get = {
    'steamid':steamid,
    }
    ret = call_api('GET', 'inv/ItemInventory/', params=get)
    jsontxt = ret.text
    inv = json.loads(jsontxt)

    return inv
    
def invDiff(old, new):
    #old array of dic with itemname and id
    #new array of dic with itemname, and other item db vars
    temp = []
    temp2 = []
    for item in old:
        temp.append(item['itemname'])
    for item in new:
        temp2.append(item['catkey'])
        
    set1 = Multiset(temp)
    set2 = Multiset(temp2)
    
    delete = set1.subtract(set2)
    add = set2.subtract(set1)
    
    print "you need to delete", len(delete), "items"
    print delete

    deleteops = []
    for item in old:
        if item['itemname'] in delete:
            deleteops.append(item['id'])
            delete.remove(item['itemname'])
    
    print "which means you need to delete", len(deleteops), "ids"
    print deleteops
    print "you need to add", len(add), "items"
    print add
    
    return {'delete':deleteops, 'add':add}
    
def addPlayer(post):
    #call api to add player, post should look like this:
    #post = {
    #'steamid':playerid, 
    #'personaname':playername, 
    #'avatar':avatar
    #}
    return call_api('POST', 'data/Players/', data=post).text
    
def addGame(post):
    #call api to add Games, post should look like this:
    #post = {
    #'appid':appid, 
    #'name':name
    #}
    return call_api('POST', 'data/Games/', data=post).text
    
def addGameInventory(post):
    #call api to add Games, post should look like this
    #post = {
    #'catkey':steamid + appid,
    #'steamid':steamid,
    #'appid':appid, 
    #'name':name
    #}
    return call_api('POST', 'inv/GameInventory/', data=post).text

def addItem(post):
    time = datetime.now()
    #call api to add items to the items database, post should look like this:
    #post = {
    #'itemname':item,
    #'itemtype':game,
    #'trading_card':'on',
    #'price':price,
    #'updated':time
    #}
    post['updated'] = time
    return call_api('POST', 'data/Items/', data=post).text
    
def updateItem(item, post):
    time = datetime.now()
    #call api to update items, post should look like this:
    #post = {
    #'itemname':item,
    #'itemtype':game,
    #'trading_card':'on',
    #'price':price,
    #'updated':time
    #}
    post['updated'] = time
    return call_api('PUT', 'data/Items/' + item + '/', data=post).text
    
def updateItemInventory(old, new):
    #itemDic is returned from getPlayerInventory
    #names[classid] = {
    #'itemname':name,
    #'itemtype':gametype,
    #'trading_card':cardflag,
    #'price':0, #cannot get price here
    #'updated':datetime.now()
    #}
    #alias for invDiff
    return invDiff(old, new)

def updateItemPrice(item, price):
    time = datetime.now()
    #call api to update price point on items
    post = {
    'itemname':item,
    'price':price,
    'updated':time
    }
    return call_api('PUT', 'data/Items/' + item + '/', data=post).text
    
def addBadge(post):
    #call api to add badges, post should look like this:
    #catkey = appid + badgeid + foil
    #post = {
    #'catkey':catkey,
    #'appid':appid,
    #'badgeid':badgeid,
    #'foiled':1,
    #'level':lvl
    #}
    return call_api('POST', 'inv/BadgeInventory/', data=post).text

def updateBadge(catkey, post):
    #call api to update level, post should look like this:
    #catkey = appid + badgeid + foil
    #post = {
    #'catkey':catkey,
    #'appid':appid,
    #'badgeid':badgeid,
    #'foiled':1,
    #'level':lvl
    #}
    return call_api('PUT', 'inv/BadgeInventory/' + catkey + '/', data=post).text
