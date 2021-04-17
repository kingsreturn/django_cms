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


# @csrf_exempt
def login_view(request):
    next = request.GET.get('next')
    form =UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request,user)
        if next:
            redirect(next)
        else:
            return redirect('/home')
    context = {
        'form': form,
    }
    return render(request,'users/login.html',context)


def index(request):
    return render(request,'users/home.html')

def log_in(request):
    if request.method == "POST":
        #login_form = UserForm(request.POST)
        form = UserCreationForm(request.POST)
        #message = ""
        if form.is_valid():
            form.save()
            #username = login_form.cleaned_data['username']
            #password = login_form.cleaned_data['password']
            #try:
                #user = models.User.objects.get(name=username)
                #if user.password == password:
                # if user.password == hash_code(password):
                    #request.session['is_login'] = True
                    #request.session['user_id'] = user.id
                    #request.session['user_name'] = user.name
                    #return redirect('/graph')
                #else:
                #message = "Passwords are not correct！"
            #except:
                #message = "User does not exist！"
            return render(request, 'users/login.html', locals())
        else:
            form=UserCreationForm()

    #login_form = UserForm()
    return render(request,'users/login.html', locals())

def new_login(request):
    return render(request,'users/new_login.html')

def register(request):
    # register is allowed only when you are not logged in, this can be changed according to different situation
    #if request.session.get('is_login', None):
        #return redirect("/index/")
    if request.method == 'POST':
        #register_form = RegisterForm(request.POST)
        register_form = UserCreationForm(request.POST)
        # message = "Please check the content！"
        # get the data from the form
        if register_form.is_valid():
            #username = register_form.cleaned_data['username']
            #password1 = register_form.cleaned_data['password1']
            #password2 = register_form.cleaned_data['password2']
            #email = register_form.cleaned_data['email']
            #sex = register_form.cleaned_data['sex']
            register_form.save()
            # check if the passwords entered is the same
            '''
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

                # when all the input are right, create the user

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                '''
                # redirect to login automatically
            return redirect('/graph/')
        else:
            register_form = UserCreationForm()
    return render(request,'users/register.html',locals())

def logout_view(request):
    logout(request)
    #if not request.session.get('is_login', None):
        #return redirect("/index/")
    #request.session.flush()
    return render (request,'users/logout.html')

def hash_code(s, salt='django'):
    h = hashlib.sha256()
    s += salt
    # update methode only accept byte typ
    h.update(s.encode())
    return h.hexdigest()
