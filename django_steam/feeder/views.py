from django.http import HttpResponse, HttpResponseNotFound
import steamclass
import apiclass
import json

def index(request):
    return HttpResponse("Index")
    
def updateProfile(request):
    if 'steamid' not in request.GET:
        return HttpResponse('steamid not specified',status=400);
    steamid = request.GET['steamid']
    if len(steamid) != 17 or not steamid.isnumeric():
        return HttpResponse('invalid steamid presented',status=400);
    
    steamid = str(steamid)
    
    #add player to db
    player = steamclass.getPlayerInfo(steamid)
    
    #check for valid response
    if not player:
        return HttpResponse('steamid not found',status=404);
    
    playername = player['personaname']
    avatar = player['avatarfull']
    post = {
    'steamid':steamid,
    'personaname':playername,
    'avatar':avatar
    }
    print apiclass.addPlayer(post)

    #All of our itterables
    gameDic = steamclass.getPlayerGames(steamid)
    itemDic = steamclass.getPlayerInventory(steamid)
    
    count = 0
    total = len(gameDic)*3 + len(itemDic) + 5
    
    def logger(count, total):
        if count % 5 == 0 or total - count < 6:
            print count, '/', total
            f = open('/var/www/steam/market.php.count', 'w')
            progress = (count / float(total)) * 100
            print progress
            f.write(str(progress))
            f.close()
            
    #add games to the games db
    for game in gameDic:
        count = count + 1
        logger(count, total)
        print apiclass.addGame(game)

    #add games to the game inventory
    for game in gameDic:
        count = count + 1
        logger(count, total)
        
        name = game['name']
        appid = game['appid']

        print "inventorying", name, " ", appid
        #call api to add Games
        post = {
        'catkey':steamid+appid,
        'steamid':steamid, 
        'appid':name
        }
        print apiclass.addGameInventory(post)


    #add badges to the badges db
    getstuff = steamclass.getPlayerBadges(steamid)

    postDic = getstuff[0]
    badgeDic = getstuff[1]
    badgeDic2 = getstuff[2]

    games = gameDic

    print "you own", len(games), "games"

    i = 1

    for game in games:
        count = count + 1
        logger(count, total)
        
        appid = str(game['appid'])
        name = game['name']
        try:
            name + "test string"
        except UnicodeEncoderError:
            name = 'unicode error'
            
        # check if the owned game has a badge
        if appid in badgeDic:
            print i, "your game", name, "is at level", badgeDic[appid]
            i += 1
            for post in postDic:
                if (post['appid'] == appid):
                    post['appid'] = name
                    print apiclass.addBadge(post)
                    print apiclass.updateBadge(post['catkey'], post)
            
        if appid in badgeDic2:
            print i, "your game", name, "(FOIL) is at level", badgeDic2[appid]
            i += 1
            for post in postDic:
                if (post['appid'] == appid):
                    post['appid'] = name
                    print apiclass.addBadge(post)
                    print apiclass.updateBadge(post['catkey'], post)


    #add items to the items db
    #itemDic = steamclass.getPlayerInventory(steamid)
    for item in itemDic:
        count = count + 1
        logger(count, total)
        print apiclass.addItem(item)

    #gen item inventory update commands
    old = apiclass.getInventory(steamid)
    new = itemDic
    dif = apiclass.invDiff(old, new)

    delete = dif['delete']
    add = dif['add']
    
    total = total + len(delete) + len(add) - 5
    logger(count, total)

    i = 1
    #delete cards
    for id in delete:
        count = count + 1
        logger(count, total)
        
        id = str(id)
        print i, id, "deleted"
        #call api to add items to the items inventory
        print call_api('DELETE', 'inv/ItemInventory/' + id + '/')
        i += 1

    i = 1    
    for item in add:
        count = count + 1
        logger(count, total)
        
        print i, item, "added"
        #call api to add items to the items inventory
        post = {
        'steamid':steamid,
        'itemname':item
        }
        print call_api('POST', 'inv/ItemInventory/', data=post).text
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