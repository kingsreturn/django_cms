from django.conf.urls import include, url
from django.contrib import admin
from . import views
#from users.views import dashboard

urlpatterns = [
    url(r"^/", include("django.contrib.auth.urls")),
    #url(r'^new_login/', views.new_login),
    url(r'^index/', views.index),
    #url(r'^accounts/login/', views.login),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^captcha', include('captcha.urls'))
    #url(r"^dashboard/", dashboard, name="dashboard"),
]
