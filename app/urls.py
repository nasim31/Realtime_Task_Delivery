
from __future__ import unicode_literals

from django.conf.urls import url
from . import views

# Create your urls here.

urlpatterns = [
	url(r'^login$',views.login,name='Main Page'),
    url(r'^manager$',views.manager,name='Main Page'),
    url(r'^delivery$',views.delivery,name='Main Page'),
    url(r'^api/getnexttask',views.getNextTask,name='api'),
    url(r'^api/deleteTask',views.deleteTask,name='api'),
    url(r'^api/getmytasksquota/(?P<username>[^/]+)/$',views.getmytasksquota,name='api'),
    url(r'^api/getmytasks/(?P<username>[^/]+)/$',views.getMyTaks,name='api'),
    url(r'^$', views.login, name='index'),
    url(r'^chat/(?P<room_name>[^/]+)/$', views.room, name='room'),
    ]
