from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('home', views.home, name="home"),
    path('logout', views.logout, name="logout"),
    path('test', views.test, name="test"),
    url(r'^sendmessage/', views.snmsg),
    url(r'^lastmessage/', views.lstmsg),
    url(r'^allmessages/', views.allmsg),
    url(r'^info/', views.info),
]
