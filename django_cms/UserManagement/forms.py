from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth import authenticate,get_user_model

User = get_user_model()

# user login form
class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','autofocus': 'autofocus',
                                                                                               'required': 'required', 'placeholder': 'User Name'}))
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','autofocus': 'autofocus',
                                                                                                   'required': 'required', 'placeholder': 'Password'}))
    #captcha = CaptchaField(label='Verification code')

    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm,self).clean(*args,**kwargs)


# user register form
class UserRegisterForm(forms.ModelForm):
    gender = (
        ('male', "male"),
        ('female', "female"),
    )
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','autofocus': 'autofocus',
                                                                                               'required': 'required', 'placeholder': 'User Name'}))
    password1 = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','autofocus': 'autofocus',
                                                                                               'required':'required','placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirm Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','autofocus': 'autofocus',
                                                                                               'required': 'required','placeholder': ' Confirm Password'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control','autofocus': 'autofocus',
                                                                                               'required': 'required','placeholder': 'Email'}))
    sex = forms.ChoiceField(label='Gender', choices=gender)
    captcha = CaptchaField(label='Verification code')


    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'password1',
            'password2'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email has already been used')
        return super(UserRegisterForm, self).clean(*args, **kwargs)
