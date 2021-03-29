from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from . import models
from .forms import UserForm

def index(request):
    pass
    return render(request,'users/home.html')

def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'users/login.html', locals())

    login_form = UserForm()
    return render(request,'users/login.html')

def register(request):
    pass
    return render(request,'users/register.html')

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')