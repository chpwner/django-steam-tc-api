from django.db import models

class Players(models.Model):
    steamid = models.CharField(primary_key=True, max_length=17)
    personaname = models.CharField(max_length=100)
    avatar = models.URLField(max_length=200)
    def __unicode__(self):
        return self.personaname

class Games(models.Model):
    appid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
	
class Items(models.Model):
    itemname = models.CharField(primary_key=True, max_length=100)
    itemtype = models.CharField(max_length=100)
    trading_card = models.BooleanField()
    price = models.FloatField()
    updated = models.DateTimeField()
    def __unicode__(self):
        return self.itemname


#this class is somewhat irrelevant since the badge name cannot be accessed	
#class Badges(models.Model):
#    badgeid = models.IntegerField(primary_key=True)
#	name = models.CharField(max_length=100)
#	appid = models.IntegerField()
	
class GameInventory(models.Model):
    catkey = models.CharField(primary_key=True, max_length=100)
    steamid = models.ForeignKey('Players')
    appid = models.ForeignKey('Games')
	
class ItemInventory(models.Model):
    steamid = models.ForeignKey('Players')
    itemname = models.ForeignKey('Items')
	
class BadgeInventory(models.Model):
    catkey = models.CharField(primary_key=True, max_length=100)
    steamid = models.ForeignKey('Players')
    appid = models.ForeignKey('Games')
    badgeid = models.IntegerField()
    foiled = models.IntegerField()
    level = models.IntegerField()
