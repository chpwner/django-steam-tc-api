#!/usr/bin/python

import sys
import steamclass
import apiclass

#enter steam id
steamid = "76561197991459756"

#add items to the items db
itemDic = steamclass.getPlayerInventory(steamid)
for item in itemDic:
    print apiclass.addItem(item)

#gen item inventory update commands
old = apiclass.getInventory(steamid)
new = itemDic
dif = apiclass.updateItemInventory(old, new)

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