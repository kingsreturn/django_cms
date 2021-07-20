from django.urls import path
from . import views
from django.conf.urls import url
from home.module.Datenvisualization import Visualization_Update
from home.module.Datenvisualization import example
from django.views.decorators.cache import cache_page

urlpatterns = [
    #path('home', views.home,name='home'),
    #path('dashboard', views.AutoUpdate,name='autoupdate'),
    #path('graph',views.graph,name = 'graph'),
    path('graph',views.Plot_diagramm.as_view(),name = 'graph'),
    path('plot',views.plot,name = 'plot'),
    path('visualization/opc',views.Plot_diagramm.as_view(),name='opc'),
    path('autoupdate',views.AutoUpdate,name='autoupdate'),
    #url(r'^plot1d/$', views.Plot1DView.as_view(), name='plot1d'),
    url(r'^plot_original/$', cache_page(60 * 15)(views.Plot1DView.as_view()), name='plot1d'),
    url(r'^plot_fft/$', views.Plotfft.as_view(), name='plot1d'),
    url(r'^plot2d/$', views.Plot2DView.as_view(), name='plot2d'),
    #url(r'^new_login/', views.new_login),
    #url(r'^plot3d/$', views.Plot3DView.as_view(), name='plot3d'),
    url(r'^plot1d_multiple/(?P<n>\d+)/$',
        views.Plot1DMultipleView.as_view(), name='plot1d_multiple'),
    url(r'^plot1d_multiple_ajax/(?P<n>\d+)/$',
        views.plot1d_multiple_ajax, name='plot1d_multiple_ajax'),
    url(r'^plotIq/$', views.PlotIqView.as_view(), name='plotIq'),
    url(r'^plot_liveview/', views.PlotLiveView.as_view(), name='plot_live'),
    url(r'^plot_live_update/$', views.plot_live_update, name='plot_live_update'),
    #url(r'^plot3d_scatter/$', views.Plot3DScatterView.as_view(), name='plot3d_scatter'),
    #plot_livepath('',)
]
