#!/usr/bin/python

import sys
import steamclass
import apiclass

#The amazing everything updater!

#enter steam id
steamid = "76561197991459756"

#add player to db
player = steamclass.getPlayerInfo(steamid)
playername = player['personaname']
avatar = player['avatarfull']
post = {
'steamid':steamid,
'personaname':playername,
'avatar':avatar
}
print apiclass.addPlayer(post)

#add games to the games db
gameDic = steamclass.getPlayerGames(steamid)
for game in gameDic:
    print apiclass.addGame(game)

#add games to the game inventory
for game in gameDic:
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
itemDic = steamclass.getPlayerInventory(steamid)
for item in itemDic:
    print apiclass.addItem(item)

#gen item inventory update commands
old = apiclass.getInventory(steamid)
new = itemDic
dif = apiclass.invDiff(old, new)

delete = dif['delete']
add = dif['add']

i = 1
#delete cards
for id in delete:
    id = str(id)
    print i, id, "deleted"
    #call api to add items to the items inventory
    print call_api('DELETE', 'inv/ItemInventory/' + id + '/')
    i += 1

i = 1    
for item in add:
    print i, item, "added"
    #call api to add items to the items inventory
    post = {
    'steamid':steamid,
    'itemname':item
    }
    print call_api('POST', 'inv/ItemInventory/', data=post).text
    i += 1