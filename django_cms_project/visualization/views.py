from django.shortcuts import render,redirect
from django.core.cache import cache
import numpy as np
import _thread
import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from datacollection.scripts.Influxdb import Influxdb
from .scripts.PlotDiagramm import PlotDiagramm as pd


# Create your views here.
def test(request):
    return render(request, 'test.html')

class historicaldata(TemplateView):
    template_name = 'historicaldata.html'

    def get_context_data(self, **kwargs):
        _db_client = Influxdb()
        _db_client.ConnnectDatabase()
        y_dataset = _db_client.Query('sensor', 'mqtt', 'numValue','-5','-4')
        number = len(y_dataset)
        x_dataset = np.linspace(0,60,number)
        hist_data = pd('Historical Sin Signal',x_dataset,'Time (s)',y_dataset,'Sin')
        #limit = lm(x_dataset,'Time',y_dataset,'Vibration')
        context = super(historicaldata, self).get_context_data(**kwargs)
        context['plot'] = hist_data.plot_linie()
        return context
