from django.shortcuts import render,redirect
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView
from .scripts.fft import FastFourierTransformation as fft
from .scripts.limit_monitor import LimitMonitoring as lm
import numpy as np
from django.contrib.messages.views import SuccessMessageMixin

from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import _thread
import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

class Plot_fft(TemplateView):
    template_name = 'fft.html'

    def get_context_data(self, **kwargs):
        x_dataset = np.linspace(0,10,100)
        y_dataset = cache.get('/test/sin')
        tranform = fft(x_dataset,'Time',y_dataset,'Vibration')
        context = super(Plot_fft, self).get_context_data(**kwargs)
        context['plot'] = tranform.plot_fft()
        messages.add_message(self.request, messages.WARNING, 'Detected Frequency : 0.5Hz')
        return context

def test(request):
    return render(request, 'test.html')

@login_required(login_url='accounts/login/')
def analyse(request):
    # todo:
    return render(request, 'test.html')

class limit_monitor(TemplateView):
    template_name = 'limit_monitor.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        #fft.generateData(fft)
        x_dataset = np.linspace(0,10,100)
        y_dataset = cache.get('/test/sin')
        limit = lm(x_dataset,'Time',y_dataset,'Vibration')
        context = super(limit_monitor, self).get_context_data(**kwargs)
        context['plot'],result= limit.plot_limit()
        messages.add_message(self.request, messages.ERROR, 'Value Above Limit:' + result)
        return context
