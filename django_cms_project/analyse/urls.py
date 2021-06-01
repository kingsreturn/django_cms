from django.urls import path
from . import views
from django.conf.urls import url
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('analyse/test', views.test, name='dataset'),
    path('analyse', views.analyse, name='analyse'),
    path('analyse/fft', views.Plot_fft.as_view(), name='fft'),
    path('analyse/limit_monitoring', views.limit_monitor.as_view(), name='limit_monitoring'),
]
