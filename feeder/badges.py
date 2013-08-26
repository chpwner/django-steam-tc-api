#!/usr/bin/python

import apiclass
import steamclass

#select steam ID
steamid = "76561197991459756"

getstuff = steamclass.getPlayerBadges(steamid)

postDic = getstuff[0]
badgeDic = getstuff[1]
badgeDic2 = getstuff[2]

for post in postDic:
    print apiclass.addBadge(post)
    print apiclass.updateBadge(post['catkey'], post)

###################the rest of this optional#######################
games = steamclass.getPlayerGames(steamid)

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
        
    if appid in badgeDic2:
        print i, "your game", name, "(FOIL) is at level", badgeDic2[appid]
        i += 1