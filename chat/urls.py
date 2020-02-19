from django.urls import path
from . import views


app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('home', views.home, name="home"),
    path('logout', views.logout, name="logout"),
    path('test', views.test, name="test")
]
