from django.urls import path
from . import views


app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('home', views.home, name="home")
]
