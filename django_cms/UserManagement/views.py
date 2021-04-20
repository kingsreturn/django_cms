from django.shortcuts import render,redirect

# Create your views here.
from django.shortcuts import render,redirect
#from . import models
#from .forms import UserForm
#from .forms import RegisterForm
import hashlib
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate,get_user_model,login,logout
from .forms import UserLoginForm,UserRegisterForm
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request):
    next = request.GET.get('next')
    form =UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request,user)
        if next:
            return redirect(next)
        else:
            return redirect('/home')
    context = {
        'form': form,
    }
    return render(request,'users/login.html',context)


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
        return redirect('/accounts/login')
    context = {
        'form': register_form,
    }

    return render(request,'users/register.html',context)

def logout_view(request):
    logout(request)
    return render (request,'users/logout.html')

def hash_code(s, salt='django'):
    h = hashlib.sha256()
    s += salt
    # update methode only accept byte typ
    h.update(s.encode())
    return h.hexdigest()
