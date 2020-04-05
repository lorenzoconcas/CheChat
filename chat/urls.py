from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


app_name = 'chat'
urlpatterns = [
    # urls delle pagine (views)
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('home', views.home, name="home"),
    path('logout', views.logout, name="logout"),
    # urls delle richieste json

    path('client_reqs/', views.client_requests, name='c_req'),


    # serve il file js sottocitato direttamente nella root
    # utile per lo scope della PWA
    # tuttavia la PWA non sarà installabile se non in localhost (vedi certificati ssl)
    path('service-worker.js',  (TemplateView.as_view(
        template_name="service-worker.js",
        content_type='application/javascript',
    )), name='service-worker.js'),
]
