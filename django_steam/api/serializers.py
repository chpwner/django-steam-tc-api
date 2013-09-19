import sys
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import *

#fields in serializes are optional apparently
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name')
        
#Steam stuff
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ('catkey', 'itemname', 'itemtype', 'game', 'trading_card', 'price', 'updated')
        #depth = 1
        
class GameSerializer(serializers.ModelSerializer):
    cards = serializers.RelatedField(many=True, read_only=True)
    class Meta:
        model = Games
        fields = ('appid', 'name', 'cards')
        #depth = 1

class PlayerSerializer(serializers.ModelSerializer):
    licenses = serializers.RelatedField(many=True, read_only=True)
    badges = serializers.RelatedField(many=True, read_only=True)
    items = serializers.RelatedField(many=True, read_only=True)
    class Meta:
        model = Players
        fields = ('steamid', 'personaname', 'avatar', 'licenses', 'badges', 'items')
        #depth = 1
        
class GameInvSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameInventory
        fields = ('catkey', 'steamid', 'appid')
        #depth = 1
        
class ItemInvSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInventory
        fields = ('id', 'steamid', 'itemname')
        #depth = 1
        
class BadgeInvSerializer(serializers.ModelSerializer):
    #appid = serializers.RelatedField() crappy serilizers don't work I hate them
    class Meta:
        model = BadgeInventory
        fields = ('catkey', 'steamid', 'appid', 'badgeid', 'foiled', 'level')
        #depth = 1
