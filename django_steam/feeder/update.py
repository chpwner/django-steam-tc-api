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

#add items to the items db
itemDic = steamclass.getPlayerInventory(steamid)
for item in itemDic:
    print apiclass.addItem(item)

#gen item inventory update commands
old = apiclass.getInventory(steamid)
new = itemDic
dif = invDiff(old, new)

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

#add games to the games db
gameDic = steamclass.getPlayerGames(steamid)
for game in gameDic:
    print apiclass.addGame(game)

#add badges to the badges db
badgeTup = steamclass.getPlayerBadges(steamid)
badgeDic = badgeTup[0]
for badge in badgeDic:
    print apiclass.addBadge(badge)