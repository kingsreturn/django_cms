"""django_cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.views.static import serve

from django.urls import path, include,re_path
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django.conf.urls import url

from django.conf import settings
import os
from django.views.static import serve as staticserve

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)




# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('datacollection.urls')),
    path('', include('home.urls')),
    path('', include('analyse.urls')),
    path('', include('dataprocess.urls')),
    path('', include('visualization.urls')),
    path('', include('users.urls')),
    path('', include('plottemplate.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('', include(router.urls)),
    path('',include('UserManagement.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if not settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ]
