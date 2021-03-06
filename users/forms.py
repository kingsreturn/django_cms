from django import forms
from captcha.fields import CaptchaField

# user login form
class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control','autofocus': 'autofocus',
                                                                                               'required': 'required', 'placeholder': 'User Name'}))
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','autofocus': 'autofocus',
                                                                                                   'required': 'required', 'placeholder': 'Password'}))
    captcha = CaptchaField(label='Verification code')

# user register form
class RegisterForm(forms.Form):
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
