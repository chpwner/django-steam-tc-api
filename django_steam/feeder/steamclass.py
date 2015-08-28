import sys
import re
import json
import urllib
import time
from datetime import datetime

#my steam api key
apikey = ''

def getPlayerInfo(steamid):
    #open url (file) resource to get profile sumarry of
    #this uses the steam api and returns a json object
    #read more about the api here http://steamcommunity.com/dev
    #
    #using python's json decoder json objects become dictionaries
    #the json object is as follows
    #profile = {response{players[{steamid:xxx, personame:xxx, avatarfull:URL, ...}]}}
    URL = urllib.urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + apikey + "&steamids=" + steamid)
    profile = json.load(URL)
    players = profile['response']['players']
    #check for null
    if players:
        #select player from array of players
        player = players[0]
        return player
    else:
        return False
    
def getPlayerGames(steamid):
    #rewrite URL to access GetOwnedGames from Steam API
    URL = urllib.urlopen("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + apikey + "&steamid=" + steamid + "&include_appinfo=1")
    profileGames = json.load(URL)
    #json decoded object:
    #profileGames = {response{game_count:xx,games[{name:gamename,appid:gameid,images,...}]}}
    #gamecount = profileGames['response']['game_count']
    retval = []

    if 'games' not in profileGames['response']:
        return retval

    gameObj = profileGames['response']['games']
    for game in gameObj:
        retval.append({'appid':str(game['appid']),'name':game['name']})
    
    #everybody has these
    retval.append({'appid':'245070','name':'Steam Summer Getaway'})
    retval.append({'appid':'267420','name':'Holiday Sale 2013'})
    
    return retval
    
def getPlayerGameList(steamid):
    #rewrite URL to access GetOwnedGames from Steam API
    URL = urllib.urlopen("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + apikey + "&steamid=" + steamid + "&include_appinfo=1")
    ret = json.load(URL)
    retval = []
    games = ret['response']['games']
    for game in games:
        retval.append(str(game['appid']))
        
    return retval

def getPlayerInventory(steamid):
    more = True
    moreStart = 0
    ret = []
    while more:
        startCMD = "?start="+str(moreStart)
        # a json renderer I found on steam
        URL = urllib.urlopen("http://steamcommunity.com/profiles/" + steamid + "/inventory/json/753/6/" + startCMD)
        
        # decode json object to dictionary
        #
        #has two components "rgInventory" = list of items possesed by the player by id
        # and "rgDescriptions" has the name of the item and the id
        # the former tells you how many items you have, 
        # the latter the names of those items
        inventory = json.load(URL)

        itemarray = []

        #Check private profile
        if 'rgInventory' not in inventory:
            return itemarray

        # inventory dictionary items
        itemsDic = inventory['rgInventory']

        #Check if inventory blank
        if not itemsDic:
            return itemarray

        #get the more and morestart values for recursive pagnation navigation
        more = inventory['more']
        moreStart = inventory['more_start']
        
        # k is key is the same as classid
        # classid is steams terminology for the type of item (ie trading card)
        # creates a list of items by their ID
        for k, item in itemsDic.iteritems():
            classid = item['classid']
            itemarray.append(classid)

        #now that we have the id, we need the description to link it to the name
        names = {}
        descriptions = inventory['rgDescriptions']

        # loop through descriptions and create association to ID
        for k, item in descriptions.iteritems():
            classid = item['classid']
            name = item['market_name']
            gametype = item['type']
            tags = item['tags']
            game = None
            appid = None
            for temp in tags:
                if temp['category_name'] == "Game":
                    game = temp['name']
                    appid = temp['internal_name'][4:]

            if gametype.find('Trading Card') > -1:
                cardflag = 'on'
            else:
                cardflag = ''
                
            names[classid] = {
            'catkey':(name+gametype).replace('/','-'),
            'itemname':name,
            'itemtype':gametype,
            'game':game,
            'trading_card':cardflag,
            'price':0, #cannot get price here
            'updated':datetime.now(),
            'appid':appid
            }
        
        #append list
        for classid in itemarray:
            ret.append(names[classid])
            
    return ret
    
def getPlayerInventoryList(steamid):
    inventory = getPlayerInventory(steamid)
    iteminv = []
    for item in inventory:
        iteminv.append(item['itemname'])
        
    return iteminv
        
def getPlayerBadges(steamid):
    #beta steam API to get badges
    # key is unique to my account, it is the api key
    # required to access the steam api
    URL = urllib.urlopen("http://api.steampowered.com/IPlayerService/GetBadges/v0001/?key=" + apikey + "&steamid=" + steamid + "&format=json")
    ret = json.load(URL)

    #python decodes json objects to dictionaries, 
    #response contains the list of badges 0,1,2...
    badges = ret['response']['badges']
    badgeDic = {}
    badgeDic2 = {}
    retval = []
    
    for badge in badges:
        # look for the key "appid" indicative of a 
        # game badge aka trading card badge
        if 'appid' in badge:
            #check for foil cards
            foil = str(badge['border_color'])
            #get game id
            appid = str(badge['appid'])
            #badgeid
            badgeid = str(badge['badgeid'])
            # game badge level
            lvl = str(badge['level'])
        
            # create a dictionary of all game badges
            if foil == "1":
                #badge is foil
                badgeDic2[appid] = lvl
                catkey = steamid + appid + badgeid + foil
                retval.append({
                'catkey':catkey,
                'steamid':steamid,
                'appid':appid,
                'badgeid':badgeid,
                'foiled':1,
                'level':lvl
                })
                
            else:
                #badge is not foil
                badgeDic[appid] = lvl
                #call api to add badges
                catkey = steamid + appid + badgeid + foil
                retval.append({
                'catkey':catkey,
                'steamid':steamid,
                'appid':appid,
                'badgeid':badgeid,
                'foiled':0,
                'level':lvl
                })
            
    return (retval, badgeDic, badgeDic2)
    
def getPlayerBadgeList(steamid):
    #beta steam API to get badges
    # key is unique to my account, it is the api key
    # required to access the steam api
    URL = urllib.urlopen("http://api.steampowered.com/IPlayerService/GetBadges/v0001/?key=" + apikey + "&steamid=" + steamid + "&format=json")
    ret = json.load(URL)
    badges = ret['response']['badges']
    retval = []
    for badge in badges:
    # look for the key "appid" indicative of a 
    # game badge aka trading card badge
        if 'appid' in badge:
            #check for foil cards
            foil = str(badge['border_color'])
            #get game id
            appid = str(badge['appid'])
            #badgeid
            badgeid = str(badge['badgeid'])
            retval.append(appid+badgeid+foil)
        
    return retval
    
def doMarketQuery(name, append):
    append = " " + append
    retval = []
    #checks for unicode errors
    try:
        safe = name.encode('utf-8')
        query = urllib.urlencode({'query': safe + append, 'start':0, 'count':99})
    except UnicodeEncodeError:
        print "unicode encode error"
        return retval
    
    t1 = datetime.now()
    #print "running steam market call on", name + append, "please wait..."
    time.sleep(15) #steam is rate limited now, so we have to slow down

    URL = urllib.urlopen("http://steamcommunity.com/market/search/render/?"+query)
    #convert json object, essentially a count and html output
    try:
        result = json.load(URL) 
    except ValueError:
        print "broken response from steam for game: " + safe
        print "code", URL.getcode()
        print "reading URL", URL.read()
        print "info", URL.info()
        return retval
    print "done with market call", datetime.now() - t1
    
    result_count = result['total_count']
    html = result['results_html']
    
    print "results: " + str(result_count)
    
    #HTML EXTRACTION
    #uses regex's to parse the HTML data
    games = re.findall(r'market_listing_game_name">.*<', html)
    items = re.findall(r'market_listing_item_name".*<', html)
    prices = re.findall(r'\$.*<', html)
    
    #checks for equivicable list sizes
    a = len(games)
    b = len(items)
    c = len(prices)

    abc = a + b + c
    valid = abc / 3
    
    #if lists are not parallel then throw an error
    if a != valid:
        sys.exit("parse error, array mismatch")
    
    #go through the parallel lists and print item (game) and price
    #ex. item = Underground (Trading Card) game=Portal 2 price=0.10
    for item, game, price in zip(items, games, prices):
        #remove html gunk
        item = item[44:-1]
        game = game[26:-1]
        price = price[1:-1]
        
        #check to see if query result is in fact for the game selected on player profile
        if game == name + " Trading Card" or game == name + " Foil Trading Card":
            #print "++" + item + " is of type " + game + " and costs $" + price
            datestr = datetime.now().strftime("%H:%M:%S %x")
            retval.append({'updated':datestr,'trading_card':True,'itemtype':game,'price':float(price),'game':name,'itemname':item})
        else:
            #print "--" + item + " is of type " + game + " and not of type " + name
            pass
   
    return retval

def scrapeID(q):
    q = str(q)

    if q[0:29] == "http://steamcommunity.com/id/":
        pass
    else:
        q = q.replace(" ","")
        q = urllib.quote_plus(q)
        q = "http://steamcommunity.com/id/" + q

    URL = urllib.urlopen(q)
    html = URL.read()

    ret = "0"
    pos = html.find('"steamid":"')

    if pos is not -1:
        pos2 = html.find('"',pos+12)
        diff = pos2 - pos
        ret = html[pos+11:pos2]

    return ret
