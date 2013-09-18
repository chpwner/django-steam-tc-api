import json
from django.db import models

class Players(models.Model):
    steamid = models.CharField(primary_key=True, max_length=17)
    personaname = models.CharField(max_length=100)
    avatar = models.URLField(max_length=200)
    def __unicode__(self):
        return self.personaname

class Games(models.Model):
    appid = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, primary_key=True)
    def __unicode__(self):
        return self.name
	
class Items(models.Model):
    catkey = models.CharField(max_length=200, primary_key=True)
    itemname = models.CharField(max_length=100)
    itemtype = models.CharField(max_length=100)
    game = models.ForeignKey('Games', related_name='cards')
    trading_card = models.BooleanField()
    price = models.FloatField()
    updated = models.DateTimeField()
    def __unicode__(self):
        retval = {
        "itemname":self.itemname,
        "itemtype":self.itemtype,
        "trading_card":self.trading_card,
        "price":self.price,
        "updated":self.updated.strftime("%I:%M:%S %p %x"),
        "game":str(self.game)
        }

        return json.dumps(retval)

        #if (self.price == 0):
        #    flag = ""
        #else:
        #    flag = str(self.price)
        #return self.itemname + " ($" + flag + ")"


#this class is somewhat irrelevant since the badge name cannot be accessed	
#class Badges(models.Model):
#    badgeid = models.IntegerField(primary_key=True)
#	name = models.CharField(max_length=100)
#	appid = models.IntegerField()
	
class GameInventory(models.Model):
    catkey = models.CharField(primary_key=True, max_length=100)
    steamid = models.ForeignKey('Players', related_name='games')
    appid = models.ForeignKey('Games', related_name='games')
    def __unicode__(self):
        return str(self.appid)
	
class ItemInventory(models.Model):
    steamid = models.ForeignKey('Players', related_name='items')
    itemname = models.ForeignKey('Items', related_name='items')
    def __unicode__(self):
        return str(self.itemname)
	
class BadgeInventory(models.Model):
    catkey = models.CharField(primary_key=True, max_length=100)
    steamid = models.ForeignKey('Players', related_name='badges')
    appid = models.ForeignKey('Games', to_field='appid', related_name='badges')
    badgeid = models.IntegerField()
    foiled = models.IntegerField()
    level = models.IntegerField()
    def __unicode__(self):
        if (self.foiled == 1):
            flag = " (Foil)"
        else:
            flag = ""
        return str(self.appid) + flag + " (Lvl:" + str(self.level) + ")"
