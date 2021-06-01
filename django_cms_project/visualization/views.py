from django.shortcuts import render,redirect
from django.core.cache import cache
import _thread
import time
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse


# Create your views here.
def test(request):
    return render(request, 'test.html')

class UploadFile(TemplateView):
    template_name = 'upload.html'

def read_csv_view(request):
    print('file is sending')
    return HttpResponse()
