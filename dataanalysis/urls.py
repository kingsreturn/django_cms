from django.urls import path
from . import views
from django.conf.urls import url
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('dataanalysis/test', views.test, name='dataset'),
    path('dataanalysis', views.analyse, name='dataanalysis'),
    path('dataanalysis/fft', views.Plot_fft.as_view(), name='fft'),
    path('dataanalysis/limit_monitoring', views.limit_monitor.as_view(), name='limit_monitoring'),
]
