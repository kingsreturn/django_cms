from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter

import logging

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView

from .module import plot_function as plots
from .module.Datenanalyse import fft as fft

logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = "home/fft.html"

class Plot1DView(TemplateView):
    template_name = 'home/fft.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot1DView, self).get_context_data(**kwargs)
        context['plot'] = fft.plot_original()
        #context['plot'] = plots.plot1d()
        return context

class Plotfft(TemplateView):
    template_name = 'home/fft.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plotfft, self).get_context_data(**kwargs)
        context['plot'] = fft.plot_fft()
        #context['plot'] = plots.plot1d()
        return context


class Plot2DView(TemplateView):
    template_name = 'home/fft.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot2DView, self).get_context_data(**kwargs)
        context['plot'] = plots.plot2d()
        return context

# Create your views here.
def home(requests):
    return render(requests, 'home/welcome.html')

def graph(requests):
    return render(requests, 'home/opc.html')

def plot(requests):
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                        mode='lines', name='test',
                        opacity=0.8, marker_color='green')],
               output_type='div')
    return render(requests, "home/plot.html", context={'plot_div': plot_div})

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
    template_name = "home/fft.html"
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

def new_login(request):
    return render(request,'home/new_login.html')
