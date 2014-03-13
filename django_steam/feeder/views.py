from django.http import HttpResponse, HttpResponseNotFound
import steamclass
import apiclass
import json
import os.path
from multiset.multiset import Multiset

def index(request):
    return HttpResponse("Index")
    
def updateProfile(request):
    def logger(count, total, file1):
        if total is 0:
            count = 1
            total = 1
        if count % 5 == 0 or total - count < 6:
            #print count, '/', total
            f = open(file1, 'w')
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
    file1 = '/var/www/steam/logger/' + steamid
    file2 = '/var/www/steam/logger/L-' + steamid

    if os.path.isfile(file2):
        return HttpResponse("an update is in progress", status=409)
        #pass
    else:
        c = open(file2, 'w')
        c.write("locked")
        c.close()

    #zero the logger
    logger(count,total, file1)
    
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
    #PUT functions as POST in this context
    #apiclass.addPlayer(post)
    #update player just incase they change their avatar
    apiclass.updatePlayer(steamid, post)
    
    count = 5
    logger(count,total, file1)

    #All of our itterables
    gameDic = steamclass.getPlayerGames(steamid)
    
    count = 10
    logger(count,total, file1)
    
    itemDic = steamclass.getPlayerInventory(steamid)
    
    count = 15
    logger(count,total, file1)
    
    badgestuff = steamclass.getPlayerBadges(steamid)
    
    count = 20
    logger(count,total, file1)

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
        #catkey is (itemname+itemtype).replace('/','-')
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
    logger(count,total, file1)
    
    ret = apiclass.call_api('GET', 'data/Items/')
    jsontxt = ret.text
    temp = json.loads(jsontxt)
    for i in temp:
        itemsOld.append(i['catkey'])
    
    count = 30
    logger(count,total, file1)
    
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
    logger(count,total, file1)
    
    itemInvOld = apiclass.getInventory(steamid)
    
    count = 40
    logger(count,total, file1)
    
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
    logger(count,total, file1)
    
    count = 0
    total = len(gameDic)*3 + len(itemDic) + 5
    
    verbose = []
    #add games to the games db
    for game in gameDic:
        appid = str(game['appid'])
        count = count + 1
        logger(count, total, file1)
        if appid in gameAdd:
            response = apiclass.addGame(game)
            verbose.append('appid: ' + appid + ' game: ' + game['name'] + ' ' + response)

    #add games to the game inventory
    for game in gameDic:
        count = count + 1
        logger(count, total, file1)
        
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
        apiclass.call_api('DELETE', 'inv/GameInventory/' + catkey + '/')


    #print "you own", len(games), "games"
    i = 1

    for game in gameDic:
        count = count + 1
        logger(count, total, file1)
        
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
                        apiclass.updateBadge(catkey, post)


    #add items to the items db
    #itemDic = steamclass.getPlayerInventory(steamid)
    for item in itemDic:
        count = count + 1
        logger(count, total, file1)
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
    logger(count, total, file1)

    i = 1
    #delete cards
    for id in delete:
        count = count + 1
        logger(count, total, file1)
        
        id = str(id)
        #print i, id, "deleted"
        #call api to add items to the items inventory
        apiclass.call_api('DELETE', 'inv/ItemInventory/' + id + '/')
        i += 1

    i = 1    
    for item in add:
        count = count + 1
        logger(count, total, file1)
        
        #print i, item, "added"
        #call api to add items to the items inventory
        post = {
        'steamid':steamid,
        'itemname':item
        }
        apiclass.call_api('POST', 'inv/ItemInventory/', data=post).text
        i += 1

    #to trick the chrome browser, run a timed command separate from this script
    os.system('sleep 30 && rm ' + file2 + ' &')
    return HttpResponse("Profile Updated/Added Successfully")#+ ", ".join(verbose))
    
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

        catkey = (item + type).replace('/','-')

        #call api to add items to the items database
        post = {
        'catkey':catkey,
        'itemname':item,
        'itemtype':type,
        'game':game,
        'trading_card':'on',
        'price':price
        }
        #PUT request functions as a POST in this context
        #apiclass.addItem(post)
        apiclass.updateItem(catkey, post)
    
    return HttpResponse(json.dumps(query),content_type="application/json")

def scrapeID(request):
    if 'q' not in request.GET:
        return HttpResponse('q not specified',status=400)

    q = request.GET['q']

    #check for bogus entries
    if (q == "Not Found!" or q == "No ID entered!" or 
        q == "Finished!" or q == "17 digit steamid required" or 
        q == "Error: another update is in progress, 409"):
        return HttpResponse('not user input',status=400)

    ret = steamclass.scrapeID(q)

    if ret != "0":
        return HttpResponse(ret)
    else:
        return HttpResponse(ret,status=404)
