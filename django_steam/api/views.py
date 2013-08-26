from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.models import *
from api.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Players.objects.all()
    serializer_class = PlayerSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GameSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemSerializer

class GameInvViewSet(viewsets.ModelViewSet):
    queryset = GameInventory.objects.all()
    serializer_class = GameInvSerializer

class ItemInvViewSet(viewsets.ModelViewSet):
    queryset = ItemInventory.objects.all()
    serializer_class = ItemInvSerializerID
    def get_queryset(self):
        queryset = ItemInventory.objects.all()
        steamid = self.request.QUERY_PARAMS.get('steamid', None)
        if steamid is not None:
            queryset = queryset.filter(steamid__steamid=steamid)
            #ItemInvViewSet.serializer_class = ItemInvSerializerID
        return queryset

class BadgeInvViewSet(viewsets.ModelViewSet):
    queryset = BadgeInventory.objects.all()
    serializer_class = BadgeInvSerializer