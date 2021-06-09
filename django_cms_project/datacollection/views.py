from django.shortcuts import render,redirect
from django.core.cache import cache
from .scripts.mqtt import Mqtt as mq
import _thread
import threading
import time
from .forms import DataQuelleForm
from .models import DataQuelle
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import DataQuelle
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.files.storage import FileSystemStorage


def ReadSinData():
    mq("/test/sin", "8.140.157.208", 8083)

def ReadCosData():
    mq("/test/cos","8.140.157.208", 8083)

def ReadData(topic):
    mq(topic,"8.140.157.208", 8083)

def print_time(threadName, delay):
    count = 0
    while count < 100:
        if count % 10 == 0:
            cache.set('messages','This is a test number:{}!'.format(count),10)
        time.sleep(delay)
        count += 1
        cache.set('messages', 'This is a test number:{}!'.format(count), 10)
        print ("%s: %s , %s" %(threadName, time.ctime(time.time()),count))




# Create your views here.
#@login_required()
def Datasets(request):
    return render(request, 'dataset.html')

def test(request):
    return render(request,'test.html')

@csrf_exempt
#@login_required()
def adddata(request):
    if request.POST:
        form = DataQuelleForm(request.POST)
        if form.is_valid():
            #is_exist= DataQuelle.objects.filter(server=form['server'],protocol=form['protocol'],variable_address=form['variable_address'])
            #if is_exist.exists():
                #messages.warning(request, 'Dataquelle is already exist in Database')
            #else:
            form.save()
            messages.info(request, 'Dataquelle is stored in Database')
            return redirect('/datasetlist')
        #server = DataQuelle_form.cleaned_data.get('server')
        #variable_address = DataQuelle_form.cleaned_data.get('variable_address')
        #variable_name = DataQuelle_form.cleaned_data.get('variable_name')
    DataQuelle_form = DataQuelleForm()
    context = {
        'form': DataQuelle_form,
    }
    return render(request, 'adddata.html', context)

#@login_required()
def datasetlist(request):
    # 创建两个线程
    try:
        # _thread.start_new_thread(ReadSinData, ())
        # _thread.start_new_thread(ReadCosData, ())
        # thread1 = threading.Thread(target=ReadData,args=("/test/sin",))
        # thread1.start()
        # thread2 = threading.Thread(target=ReadData, args=("/test/cos",))
        # thread2.start()
        client1 = mq("/test/sin", "8.140.157.208", 8083)
        client2 = mq("/test/cos", "8.140.157.208", 8083)
    # _thread.start_new_thread(ReadData, ("/test/sin"))
    # time.sleep(1)
    # _thread.start_new_thread(ReadData, ("/test/cos"))

    except:
        print("Error: Thread start failed!")


    list = DataQuelle.objects.all()
    number = list.count()
    context = {
        'content': list
    }
    return render(request,'datasetlist.html',context=context)

def dashboard(request):
    pass
    return render(request,'datasetlist.html')

class UploadFile(TemplateView):
    template_name = 'upload.html'


def read_csv_view(request):
    print('file is sending')
    return HttpResponse()


def dropzoneuploads(request):
    if request.method == 'POST':
        files = [request.FILES.get('file[%d]' % i)
                 for i in range(0, len(request.FILES))]
        #inputs obtained from form are grabbed here, similarly other data can be gathered
        abc = request.POST['abc']
        # location where you want to upload your files
        folder = 'my_folder'
        fs = FileSystemStorage(location=folder)
        for f in files:
            filename = fs.save(f.name, f)
    data = {'status': 'success'}
    response = JsonResponse(data)
    return response
