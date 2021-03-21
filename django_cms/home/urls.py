from django.urls import path
from . import views
from home.dash_apps.finished_apps import simpleexample
from home.dash_apps.finished_apps import opc
from home.dash_apps.finished_apps import secondexample


urlpatterns = [
    path('home', views.home,name='home'),
    path('graph',views.graph,name = 'graph')
    #path('',)
]