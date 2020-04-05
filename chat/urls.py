from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'chat'
urlpatterns = [
    # urls delle pagine (views)
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('home', views.home, name="home"),
    path('logout', views.logout, name="logout"),
    # urls delle richieste json
    # url(r'^client_reqs/', views.client_requests),
    path('client_reqs/', views.client_requests, name='c_req'),
]
