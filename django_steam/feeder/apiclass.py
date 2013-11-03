import json
import requests
import urllib
#import hashlib for the debug logger
from datetime import datetime
from multiset.multiset import Multiset

def call_api(method, url, **kwargs):
    #look for '/' in catkeys, should be accounted for elsewhere
    #if 'data' in kwargs:
    #   if 'catkey' in kwargs['data']:
    #        if not kwargs['data']['catkey'].find('/') == -1:
    #            print kwargs['data']['catkey']

    #ha ha, deleted the password
    kwargs['auth'] = ('apiadmin', '')
    ret = requests.request(method, 'http://127.0.0.1/'+url, **kwargs)

    #Debug Logger
    #u = ret.text
    #text = u.encode('utf-8')
    #fileH = hashlib.sha224(text).hexdigest()
    #file1 = fileH[0:8]
    #file1 = "apilog"
    #f = open('/tmp/'+method+file1,'a')
    #f.write(text+"\n")
    #f.close()

    return ret

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
    
    #print "you need to delete", len(delete), "items"
    #print delete

    deleteops = []
    for item in old:
        if item['itemname'] in delete:
            deleteops.append(item['id'])
            delete.remove(item['itemname'])
    
    #print "which means you need to delete", len(deleteops), "ids"
    #print deleteops
    #print "you need to add", len(add), "items"
    #print add
    
    return {'delete':deleteops, 'add':add}
    
def addPlayer(post):
    #call api to add player, post should look like this:
    #post = {
    #'steamid':playerid, 
    #'personaname':playername, 
    #'avatar':avatar
    #}
    return call_api('POST', 'data/Players/', data=post).text
    
def updatePlayer(steamid, post):
    #call api to add player, post should look like this:
    #post = {
    #'steamid':playerid, 
    #'personaname':playername, 
    #'avatar':avatar
    #}
    return call_api('PUT', 'data/Players/'+steamid+'/', data=post).text
    
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
    #apply the '/' fix to the catkey and unicode
    #catkey should not require this as it should be taken care of elsewhere
    item = urllib.quote(item.encode('utf-8'))
    if not item.find('/') == -1:
        print item
        item.replace('/','-')
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
