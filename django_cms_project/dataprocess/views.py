from django.shortcuts import render,redirect
from django.core.cache import cache
import _thread
import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .scripts import processed_mqtt
from datacollection.models import DataQuelle


# Create your views here.
def processed(request):
    list = DataQuelle.objects.all()
    context = {
        'content': list
    }
    return render(request, 'process_datasets.html',context=context)

def processed_opc(request):
    return render(request, 'test.html')

def processed_mqtt(request):
    return render(request, 'processed_mqtt.html')
