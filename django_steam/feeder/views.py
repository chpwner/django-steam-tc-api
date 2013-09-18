from django.http import HttpResponse, HttpResponseNotFound
import steamclass
import apiclass
import json

def index(request):
    return HttpResponse("Index")
    
def updateGames(request):
    return HttpResponse("profile games updated successfully")
    
def updateBadges(request):
    return HttpResponse("profile badges updated successfully")
    
def updateInventory(request):
    return HttpResponse("profile inventory updated successfully")
    
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