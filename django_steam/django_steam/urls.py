from django.conf.urls import patterns, url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router2 = routers.DefaultRouter()
router3 = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router2.register(r'Players', views.PlayerViewSet)
router2.register(r'Games', views.GameViewSet)
router2.register(r'Items', views.ItemViewSet)
router3.register(r'GameInventory', views.GameInvViewSet)
router3.register(r'ItemInventory', views.ItemInvViewSet)
router3.register(r'BadgeInventory', views.BadgeInvViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
from django.http import HttpResponse
urlpatterns = patterns('',
    url(r'^$', lambda x: HttpResponse('<a href="auth/">auth</a> \
    <a href="data/">data</a> <a href="inv/">inv</a>')),
    url(r'^auth/', include(router.urls)),
    url(r'^data/', include(router2.urls)),
    url(r'^inv/', include(router3.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)