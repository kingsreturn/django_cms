from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
from UserManagement.decorators import unauthenticated_user, allowed_users
import logging

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView

from .module.Datenvisualization import Datavisualization as plots
from .module.Datenanalyse.fft import FastFourierTransformation as fft
#from .module.SignalSimulator import SignalSimulator as ss
#from .module.Datenvisualization import Datavisualization as plot_diagramm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import caches
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import _thread
import time
from .module.Datencollection.mqtt import Mqtt as mq


logger = logging.getLogger(__name__)

# Create your views here.
@login_required(login_url='accounts/login/')
def home(request):
    messages.info(request,'This is a test Message!')
    messages.warning(request, 'This is a test Warning!')
    messages.error(request, 'This is a test Error!')

    return render(request, 'home/home.html')

@login_required(login_url='accounts/login/')
def AutoUpdate(request):
    return render(request, 'home/autoupdate.html')


@login_required(login_url='accounts/login/')
def graph(requests):
    return render(requests, 'home/opc.html')

@login_required(login_url='accounts/login/')
def Dataset(request):
    return render(request, 'home/dataset.html')

def plot(requests):
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
    return render(requests, "home/plot.html", context={'plot_div': plot_div})

class IndexView(TemplateView):
    template_name = "home/plot_live.html"


class Plot1DView(TemplateView):
    template_name = 'home/fft.html'
    def get_context_data(self, **kwargs):
        fft.generateData(fft)
        # Call the base implementation first to get a context
        context = super(Plot1DView, self).get_context_data(**kwargs)
        context['plot'] = fft.plot_original(fft,cache.get('time'), cache.get('signal'))
        return context


# @method_decorator(login_required, name='dispatch')
class Plot_diagramm(LoginRequiredMixin, TemplateView):
#class Plot_diagramm(TemplateView):
    template_name = 'home/fft.html'
    #login_url = '/login/'
    #redirect_field_name = 'redirect_to'

    # @login_required(redirect_field_name='/login/')
    # @cache_page(60 * 15)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot_diagramm, self).get_context_data(**kwargs)
        context['plot'] = plots.plot_diagramm([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                        [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
                                        'Time (s)','Function')
        #context['plot'] = plots.plot1d()
        return context


class Plotfft(TemplateView):
    template_name = 'home/fft.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        fft.generateData(fft)
        context = super(Plotfft, self).get_context_data(**kwargs)
        #context['plot'] = fft.plot_fft(fft,cache.get('signal'))
        context['plot'] = fft.plot_fft(fft,cache.get('/test/sin'))
        #context['plot'] = plots.plot1d()
        return context


class Plot2DView(TemplateView):
    template_name = 'home/fft.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot2DView, self).get_context_data(**kwargs)
        context['plot'] = plots.plot2d()
        return context



class Plot3DView(TemplateView):
    template_name = "home/fft.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot3DView, self).get_context_data(**kwargs)
        context['plot'] = plots.plot3d()
        return context


class Plot1DMultipleView(TemplateView):
    template_name = "home/fft.html"

    def get_context_data(self, **kwargs):
        n = int(kwargs['n'])
        # Call the base implementation first to get a context
        context = super(Plot1DMultipleView, self).get_context_data(**kwargs)
        context['plot'] = plots.plot1d_multiple(n)
        return context


def plot1d_multiple_ajax(request, n):
    """
    Only handles AJAX queries
    """
    logger.debug("Plotting {} plots.".format(n))
    return HttpResponse(plots.plot1d_multiple(int(n)))


class PlotIqView(TemplateView):
    template_name = "home/fft.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotIqView, self).get_context_data(**kwargs)
        context['plot'] = plots.plotIq()
        return context


class PlotLiveView(TemplateView):
    template_name = "home/plot_live.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PlotLiveView, self).get_context_data(**kwargs)
        context['plot'] = plots.plotLive()
        return context


def plot_live_update(request):
    '''
    Handle ajax call to update the live plot
    '''
    if request.is_ajax():
        logger.debug("Live plot updated...")
        data = plots.live_plot_get_data_serialized()
        # In order to allow non-dict objects to be serialized set the safe
        # parameter to False
        return JsonResponse([data], safe=False)
    else:
        return HttpResponseBadRequest()

class Plot3DScatterView(TemplateView):
    template_name = "home/fft.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot3DScatterView, self).get_context_data(**kwargs)
        context['plot'] = plots.plot3D_scatter
        return context

def warning(dataset,limit):
    warnstatus = False
    for value in dataset:
        if value > limit:
            warnstatus
    return warnstatus

