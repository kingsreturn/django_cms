from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from . import models
from .forms import UserForm
from .forms import RegisterForm
import hashlib

def index(request):
    return render(request,'users/home.html')

def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = ""
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return redirect('/graph')
                else:
                    message = "Passwords are not correct！"
            except:
                message = "User does not exist！"
        return render(request, 'users/login.html', locals())

    login_form = UserForm()
    return render(request,'users/login.html', locals())

def new_login(request):
    return render(request,'users/new_login.html')

def register(request):
    # register is allowed only when you are not logged in, this can be changed according to different situation
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "Please check the content！"
        # get the data from the form
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            # check if the passwords entered is the same
            if password1 != password2:
                message = "Passwords entered are different！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                # check if user name is registered
                if same_name_user:
                    message = 'The user already exists, please re-select the user name！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                # check if email address is registered
                if same_email_user:
                    message = 'This email address has already been registered, please use another email address！'
                    return render(request, 'login/register.html', locals())

                # when all the iput are right, create the user

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                # redirect to login automatically
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request,'users/register.html',locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')

def hash_code(s, salt='django'):
    h = hashlib.sha256()
    s += salt
    # update methode only accept byte typ
    h.update(s.encode())
    return h.hexdigest()
