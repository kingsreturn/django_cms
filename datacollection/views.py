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
from django.shortcuts import redirect


# Create data collection thread
def collectdata():
    try:
        client1 = mq("/test/sin", "8.140.157.208", 8083)
        client2 = mq("/test/cos", "8.140.157.208", 8083)
        client3 = mq("/test/sawtooth", "8.140.157.208", 8083)
    except:
        print("Error: Thread start failed!")

class myThread(threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, address, client):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.address = address
        self.status = True
        #self.client = client
    def run(self):
        if hasattr(self, 'client'):
            self.client.on_disconnect()
            time.sleep(2)
        while self.status:
            print("Starting " + self.address)
            self.client = mq(self.address, "8.140.157.208", 8083)
            time.sleep(180)
            self.client.on_disconnect()
            print("Exiting " + self.address)

    def stop(self):
        self.client.on_disconnect()

# create data collection thread
thread1 = myThread(1, "/test/sin", 1)
thread2 = myThread(2, "/test/cos", 2)
thread3 = myThread(2, "/test/sawtooth", 3)

def collectdata1():
    thread1 = myThread(1, "/test/sin", 1)
    thread2 = myThread(2, "/test/cos", 2)
    thread3 = myThread(2, "/test/sawtooth", 3)
    # start data collection thread
    try:
        thread1.start()
        thread2.start()
        thread3.start()
        print('Thread start success!')
    except:
        print("Error: Thread start failed!")

def stopcollect():
    try:
        thread1.stop()
        thread2.stop()
        thread3.stop()
        print('Thread stop success!')
    except:
        print('Thread stop failed!')


collectdata()
sin = cache.get('/test/sin/value')
#cos = cache.get('/test/cos/value')
#sawtooth = cache.get('/test/sawtooth/value')
print(sin)

def home(request):
    #stopcollect()
    #time.sleep(10)
    #collectdata()
    return redirect(dashboard)

#@login_required()
def Datasets(request):
    return render(request, 'dataset.html')

def test(request):
    return render(request,'test.html')

#@login_required(login_url='accounts/login/')
def dashboard(request):
    #collectdata()
    #time.sleep(5)
    return render(request, 'dashboard.html')

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
    list = DataQuelle.objects.all()
    number = list.count()
    context = {
        'content': list
    }
    return render(request,'datasetlist.html',context=context)

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
