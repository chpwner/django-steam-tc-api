#!/usr/bin/python

import sys
import steamclass
import apiclass

#set steamid
#me
steamid = "76561197991459756"
#rizzo
#steamid = "76561197970539274"

player = steamclass.getPlayerInfo(steamid)

playerid = player['steamid']
playername = player['personaname']
avatar = player['avatarfull']

#add player to database
post = {
'steamid':playerid,
'personaname':playername,
'avatar':avatar,
}
print apiclass.addPlayer(post)

print "Welcome palyer number", playerid, "\n\na.k.a.\n\n", playername, "\n\nThis program will extract your game libaray and \nperform a brute force store search for applicaable trading cards\n"

games = steamclass.getPlayerGames(steamid)

print playername, "owns", len(games), "games"

gamearr = []
#loop through all games owned by the steam ID
for game in games:
    name = game['name']
    appid = game['appid']
    gamearr.append(appid)

    print "adding", name
    #call api to add Games
    post = {
    'appid':appid, 
    'name':name
    }
    print apiclass.addGame(post)
    
    print "inventorying",name
    #call api to add to game inventory
    post = {
    'appid':name, #override with name primary key
    'steamid':steamid,
    'catkey':steamid + appid
    }
    print apiclass.addGameInventory(post)

    print
    query = steamclass.doMarketQuery(name, 'trading card')
    print
    
    for dic in query:
        item = dic['item'] #str
        type = dic['type'] #str
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
        print apiclass.addItem(post)
        
        #call api to update the items database
        post = {
        'catkey':catkey,
        'itemname':item,
        'itemtype':type,
        'game':game,
        'trading_card':'on',
        'price':price
        }
        print apiclass.updateItem(catkey, post)