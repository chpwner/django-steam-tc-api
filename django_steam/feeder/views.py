from django.http import HttpResponse, HttpResponseNotFound
import steamclass
import apiclass
import json
import os.path
import sys
from multiset.multiset import Multiset

def index(request):
    return HttpResponse("Index")
    
def updateProfile(request):
    def logger(count, total, file):
        if count % 5 == 0 or total - count < 6:
            #print count, '/', total
            f = open(file, 'w')
            progress = (count / float(total)) * 100
            #print progress
            f.write(str(progress))
            f.close()

    if 'steamid' not in request.GET:
        return HttpResponse('steamid not specified',status=400)
    steamid = request.GET['steamid']
    if len(steamid) != 17 or not steamid.isnumeric():
        return HttpResponse('invalid steamid presented',status=400)
    
    steamid = str(steamid)
    
    count = 0
    total = 100
    file = '/var/www/steam/logger/' + steamid
    logger(count,total, file)
    
    #add player to db
    player = steamclass.getPlayerInfo(steamid)
    
    #check for valid response
    if not player:
        return HttpResponse('steamid not found',status=404)
    
    playername = player['personaname']
    avatar = player['avatarfull']
    post = {
    'steamid':steamid,
    'personaname':playername,
    'avatar':avatar
    }
    apiclass.addPlayer(post)
    #update player just incase they change their avatar
    apiclass.updatePlayer(steamid, post)
    
    count = 5
    logger(count,total, file)

    #All of our itterables
    gameDic = steamclass.getPlayerGames(steamid)
    
    count = 10
    logger(count,total, file)
    
    itemDic = steamclass.getPlayerInventory(steamid)
    
    count = 15
    logger(count,total, file)
    
    badgestuff = steamclass.getPlayerBadges(steamid)
    
    count = 20
    logger(count,total, file)

    postDic = badgestuff[0]
    badgeDic = badgestuff[1]
    badgeDic2 = badgestuff[2]
    
    #generate simple lists of respective primary keys
    gameInv = []
    items = []
    badgeInv = []
    
    for game in gameDic:
        gameInv.append(str(game['appid']))
        
    for item in itemDic:
        appid = str(item['appid'])
        game = item['game']
        catkey = item['catkey']
        if catkey not in items:
            items.append(catkey)
        #catkey is itemname+itemtype
        #append to games where applicable
        if appid not in gameInv:
            gameDic.append({'name':game, 'appid':appid})
			# if they player has items for a game, this makes that game appear to
			#  be owned i.e. the person is collecting for a game they do not own, 
			#  the usefulness of this is obtuse and I am considering removing it.
            gameInv.append(appid)
        
    for badge in postDic:
        badgeInv.append(badge['catkey']+str(badge['level']))
        #catkey is steamid+appid+1+foiled(0 or 1)+level(for this instance only)
        
    #get old lists from the database
    gamesOld = []
    itemsOld = []
    gameInvOld = []
    badgeInvOld = []
    
    ret = apiclass.call_api('GET', 'data/Games/')
    jsontxt = ret.text
    temp = json.loads(jsontxt)
    for i in temp:
        gamesOld.append(str(i['appid']))
        
    count = 25
    logger(count,total, file)
        
    ret = apiclass.call_api('GET', 'data/Items/')
    jsontxt = ret.text
    temp = json.loads(jsontxt)
    for i in temp:
        itemsOld.append(i['catkey'])
        
    count = 30
    logger(count,total, file)
        
    get = {
    'steamid':steamid,
    }
    ret = apiclass.call_api('GET', 'inv/GameInventory/', params=get)
    jsontxt = ret.text
    temp = json.loads(jsontxt)
    for i in temp:
        catkey = i['catkey']
        if catkey[0:17] == steamid:
            gameInvOld.append(catkey[17:])
            
    count = 35
    logger(count,total, file)
            
    itemInvOld = apiclass.getInventory(steamid)
            
    count = 40
    logger(count,total, file)
            
    get = {
    'steamid':steamid,
    }
    ret = apiclass.call_api('GET', 'inv/BadgeInventory/', params=get)
    jsontxt = ret.text
    temp = json.loads(jsontxt)
    for i in temp:
        if i['steamid'] == steamid:
            badgeInvOld.append(i['catkey']+str(i['level']))
    
    #generate differences
    old = Multiset(gamesOld)
    new = Multiset(gameInv)
    gameAdd = new.subtract(old)
    
    old = Multiset(itemsOld)
    new = Multiset(items)
    itemAdd = new.subtract(old)
    
    old = Multiset(gameInvOld)
    new = Multiset(gameInv)
    gameInvAdd = new.subtract(old)
    gameInvDel = old.subtract(new)
    
    old = Multiset(badgeInvOld)
    new = Multiset(badgeInv)
    badgeAdd = new.subtract(old)
    
    count = 50
    logger(count,total, file)
    
    count = 0
    total = len(gameDic)*3 + len(itemDic) + 5
            
    #add games to the games db
    for game in gameDic:
        appid = str(game['appid'])
        count = count + 1
        logger(count, total, file)
        if appid in gameAdd:
            apiclass.addGame(game)

    #add games to the game inventory
    for game in gameDic:
        count = count + 1
        logger(count, total, file)
        
        name = game['name']
        appid = str(game['appid'])

        #print "inventorying", name, " ", appid
        #call api to add Games
        post = {
        'catkey':steamid+appid,
        'steamid':steamid, 
        'appid':name
        }
        if appid in gameInvAdd:
            apiclass.addGameInventory(post)
            
    #remove free trial games from inventory
    for appid in gameInvDel:
        catkey = steamid + appid
        apiclass.call_api('DELETE', 'inv/ItemInventory/' + catkey + '/')


    #print "you own", len(games), "games"
    i = 1

    for game in gameDic:
        count = count + 1
        logger(count, total, file)
        
        appid = str(game['appid'])
        name = game['name']
        try:
            name + "test string"
        except UnicodeEncoderError:
            name = 'unicode error'
            
        # check if the owned game has a badge
        if appid in badgeDic:
            #print i, "your game", name, "is at level", badgeDic[appid]
            i += 1
            for post in postDic:
                if (post['appid'] == appid):
                    #override id for primary key
                    post['appid'] = name
                    catkey = post['catkey']
                    compare = catkey + str(post['level'])
                    if compare in badgeAdd:
                        apiclass.addBadge(post)
                        apiclass.updateBadge(catkey, post)
            
        if appid in badgeDic2:
            #print i, "your game", name, "(FOIL) is at level", badgeDic2[appid]
            i += 1
            for post in postDic:
                if (post['appid'] == appid):
                    #override id for primary key
                    post['appid'] = name
                    catkey = post['catkey']
                    compare = catkey + str(post['level'])
                    if compare in badgeAdd:
                        apiclass.addBadge(post)
                        apiclass.updateBadge(catkey, post)


    #add items to the items db
    #itemDic = steamclass.getPlayerInventory(steamid)
    for item in itemDic:
        count = count + 1
        logger(count, total, file)
        if item['catkey'] in itemAdd:
            apiclass.addItem(item)

    #gen item inventory update commands
    #old = apiclass.getInventory(steamid)
    old = itemInvOld
    new = itemDic
    dif = apiclass.invDiff(old, new)

    delete = dif['delete']
    add = dif['add']
    
    total = total + len(delete) + len(add) - 5
    logger(count, total, file)

    i = 1
    #delete cards
    for id in delete:
        count = count + 1
        logger(count, total, file)
        
        id = str(id)
        #print i, id, "deleted"
        #call api to add items to the items inventory
        apiclass.call_api('DELETE', 'inv/ItemInventory/' + id + '/')
        i += 1

    i = 1    
    for item in add:
        count = count + 1
        logger(count, total, file)
        
        #print i, item, "added"
        #call api to add items to the items inventory
        post = {
        'steamid':steamid,
        'itemname':item
        }
        apiclass.call_api('POST', 'inv/ItemInventory/', data=post).text
        i += 1
        
    return HttpResponse("Profile Updated/Added Successfully")
    
def updatePrice(request):
    if 'game' not in request.GET:
        return HttpResponse('game not specified',status=400);
    name = request.GET['game']
    if name == '':
        return HttpResponse('game not specified',status=400);
        
    query = steamclass.doMarketQuery(name, 'Trading Card')
    
    if not query:
        return HttpResponseNotFound(name)

    for dic in query:
        item = dic['itemname'] #str
        type = dic['itemtype'] #str
        game = dic['game'] #str
        price = dic['price'] #float

        catkey = item + type

        #call api to add items to the items database
        post = {
        'catkey':catkey,
        'itemname':item,
        'itemtype':type,
        'game':game,
        'trading_card':'on',
        'price':price
        }
        apiclass.addItem(post)

        #call api to update the items database
        post = {
        'catkey':catkey,
        'itemname':item,
        'itemtype':type,
        'game':game,
        'trading_card':'on',
        'price':price
        }
        apiclass.updateItem(catkey, post)
    return HttpResponse(json.dumps(query),content_type="application/json")