from django.urls import path
from . import views
from django.conf.urls import url
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('Dataset', views.Datasets, name='dataset'),
    path('RohData/opc',views.test, name='dataset'),
    path('RohData/mqtt',views.test, name='dataset'),
    path('adddata',views.adddata,name='adddata'),
    path('datasetlist',views.datasetlist,name='datasetlist'),
    path('visualization',views.dashboard,name='datasetlist'),
    path('upload/', views.UploadFile.as_view(), name='upload'),
    path('read_csv/', views.read_csv_view, name='read_csv')
]




