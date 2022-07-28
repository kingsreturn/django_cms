from django.urls import path
from . import views
from django.conf.urls import url
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('visulization/test', views.test, name='dataset'),
    path('visulization/historicaldata', views.historicaldata.as_view(), name='historicaldata'),
]
