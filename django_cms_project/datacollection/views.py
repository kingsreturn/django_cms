from django.shortcuts import render,redirect
from django.core.cache import cache
from .scripte.mqtt import Mqtt as mq
import _thread
import time
from .forms import DataQuelleForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import DataQuelle


def ReadSinData():
    topic1="/test/sin"
    mqtt_client = mq(topic1)
    mqtt_client.client.connect("8.140.157.208", 8083, 60)
    mqtt_client.client.subscribe(topic1, 0)
    mqtt_client.client.loop_forever()

def ReadCosData():
    topic2 = "/test/cos"
    mqtt_client = mq(topic2)
    mqtt_client.client.connect("8.140.157.208", 8083, 60)
    mqtt_client.client.subscribe(topic2, 0)
    mqtt_client.client.loop_forever()

def print_time(threadName, delay):
    count = 0
    while count < 100:
        if count % 10 == 0:
            cache.set('messages','This is a test number:{}!'.format(count),10)
        time.sleep(delay)
        count += 1
        cache.set('messages', 'This is a test number:{}!'.format(count), 10)
        print ("%s: %s , %s" %(threadName, time.ctime(time.time()),count))

# 创建两个线程
try:
   _thread.start_new_thread(ReadSinData, ())
   _thread.start_new_thread(ReadCosData, ())

except:
   print ("Error: 无法启动线程")


# Create your views here.
def Datasets(request):
    return render(request, 'dataset.html')

def test(request):
    return render(request,'test.html')

@csrf_exempt
def adddata(request):
    if request.POST:
        form = DataQuelleForm(request.POST)
        if form.is_valid():
            is_exist= DataQuelle.objects.filter(server=form['server'],protocol=form['protocol'],variable_address=form['variable_address'])
            if is_exist.exists():
                messages.warning(request, 'Dataquelle is already exist in Database')
            else:
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

def datasetlist(request):
    # todo: list the dataset in database
    return render(request,'todo.html')
