from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import *

#serializes are optional apparently
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        #fields = ('steamid', 'personaname', 'avatar')
        
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        #fields = ('appid', 'name')
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        #fields = ('itemname', 'itemtype', 'trading_card', 'price', 'updated')
        
class GameInvSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameInventory
        #fields = ('catkey', 'steamid', 'appid')
        
class ItemInvSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInventory
        #fields = ('steamid', 'itemname')
        
class ItemInvSerializerID(serializers.ModelSerializer):
    class Meta:
        model = ItemInventory
        #fields = ('id', 'steamid', 'itemname')
        
class BadgeInvSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeInventory
        #fields = ('catkey', 'steamid', 'appid', 'badgeid', 'foiled', 'level')
