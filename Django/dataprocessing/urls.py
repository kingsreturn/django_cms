from django.urls import path
from . import views
from django.conf.urls import url
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('processed', views.processed, name='dataset'),
    path('processed/opc', views.processed_mqtt, name='dataset'),
    path('processed/mqtt',views.processed_mqtt, name='dataset'),
]
