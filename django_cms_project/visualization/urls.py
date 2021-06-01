from django.urls import path
from . import views
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from .views import UploadFile

urlpatterns = [
    path('visulization/test', views.test, name='dataset'),
    path('upload/', views.UploadFile.as_view(), name='upload'),
    path('read_csv/',views.read_csv_view, name='read_csv')
]
