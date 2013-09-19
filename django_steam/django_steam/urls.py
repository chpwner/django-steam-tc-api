from django.conf.urls import patterns, url, include
from rest_framework import routers
import api.views
import feeder.views

router = routers.DefaultRouter()
router2 = routers.DefaultRouter()
router3 = routers.DefaultRouter()
router.register(r'users', api.views.UserViewSet)
router.register(r'groups', api.views.GroupViewSet)
router2.register(r'Players', api.views.PlayerViewSet)
router2.register(r'Games', api.views.GameViewSet)
router2.register(r'Items', api.views.ItemViewSet)
router3.register(r'GameInventory', api.views.GameInvViewSet)
router3.register(r'ItemInventory', api.views.ItemInvViewSet)
router3.register(r'BadgeInventory', api.views.BadgeInvViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
from django.http import HttpResponse
urlpatterns = patterns('',
    url(r'^$', lambda x: HttpResponse('<a href="auth/">auth</a> \
    <a href="data/">data</a> <a href="inv/">inv</a>')),
    url(r'^auth/', include(router.urls)),
    url(r'^data/', include(router2.urls)),
    url(r'^inv/', include(router3.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^update/$', feeder.views.index, name="Update Index"),
    url(r'^update/profile/', feeder.views.updateProfile, name="Update Profile"),
    url(r'^update/price/', feeder.views.updatePrice, name="Update Item Price")
)