from django.shortcuts import render

# Create your views here.
def home(requests):
    return render(requests, 'home/welcome.html')

def graph(requests):
    return render(requests, 'home/opc.html')
