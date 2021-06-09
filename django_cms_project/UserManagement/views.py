from django.shortcuts import render,redirect
#from . import models
#from .forms import UserForm
#from .forms import RegisterForm
import hashlib
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import AnonymousUser,User
from django.contrib.auth import authenticate,get_user_model,login,logout,get_user
from .forms import UserLoginForm,UserRegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import Template,Context
from .decorators import unauthenticated_user,allowed_users, admin_only
from django.contrib.auth.decorators import login_required


@csrf_exempt
@unauthenticated_user
def login_view(request):
    next = request.GET.get('next')
    form =UserLoginForm(request.POST or None)
    message=''
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect(next)
        else:
            return redirect('/datasetlist')
        #user = authenticate(username=username,password=password)
        #login(request,user)
        #if next:
            #return redirect(next)
        #else:
            #return redirect('/home')
    context = {
        'form': form,
    }
    return render(request,'login.html',locals())


def index(request):
    return render(request,'users/home.html')

@csrf_exempt
def register_view(request):
    next = request.GET.get('next')
    register_form = UserRegisterForm(request.POST or None)
    if register_form.is_valid():
        user = register_form.save(commit=False)
        password = register_form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username,password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/userlist')
    context = {
        'form': register_form,
    }

    return render(request,'register.html',context)

def logout_view(request):
    user = get_user(request)

    logout(request)
    request.session.flush()
    print('you are log out from cms!')
    #request.user = AnonymousUser
    return render(request,'logout.html')

def hash_code(s, salt='django'):
    h = hashlib.sha256()
    s += salt
    # update methode only accept byte typ
    h.update(s.encode())
    return h.hexdigest()

def userlist(request):
    User = get_user_model()
    result = User.objects.all()
    #template = Template('userlist.html')
    #html = template.render(Context({'content': result}))
    context = {
        'content':result,
    }
    return render(request,'userlist.html',context=context)

def adduser(request):
    return render(request,'todo.html')

@csrf_exempt
def delete_user(request,id):
    User =get_user_model()
    if request.method == 'GET':
        try:
            result = User.objects.filter(id=id)
            result.delete()
            return HttpResponse('success')
        except:
            return HttpResponse('fail')
#获取修改用户的页面
@login_required(login_url='accounts/login/')
def editUser(request,id):
    User = get_user_model()
    if request.method == 'GET':
        #result = User.objects.filter(id)
        result = User.objects.filter(id=id)
        #print("需要修改的用户名为：".format(result))
        template = Template('updateuser.html')
        html = template.render({'content': result})
        return HttpResponse(html)

@login_required(login_url='accounts/login/')
def notpermitted(request):
    return render(request,'NotPermitted.html')
