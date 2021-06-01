from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from . import views
#from users.views import dashboard

urlpatterns = [
    #path("accounts/"),
    url(r'^accounts/index/', views.index),
    # url(r'^accounts/login/', views.login),
    url(r'^accounts/login/', views.login_view),
    url(r'^accounts/register/', views.register_view),
    url(r'^accounts/logout/', views.logout_view),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r'^userlist', views.userlist),
    url(r'^adduser', views.register_view),
    url(r'^notpermitted', views.register_view),
    #url(r'^createUser/$',views.create_user,name='createUser'),
    url(r'^deleteUser/(.+)/$',views.delete_user,name='deleteUser'),
    #url(r'^changePassword/$',views.change_password,name='changePassword'),
    url(r'^editUser/(.+)/$',views.editUser,name='editUser'),
    #url(r'^listUser/$',views.listUser,name='listUser'),

    #url(r'^new_login/', views.new_login),
    #url(r'^index/', views.index),
    #url(r'^login/', views.login),
    #url(r'^register/', views.register),
    #url(r'^logout/', views.logout),
    url(r'^captcha', include('captcha.urls'))
    #url(r"^dashboard/", dashboard, name="dashboard"),
]
