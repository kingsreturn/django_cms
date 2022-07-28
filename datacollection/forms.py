from django import forms
from django.forms import ModelForm
#from captcha.fields import CaptchaField
#from django.contrib.auth import authenticate, get_user_model
from .models import DataQuelle
#User = get_user_model()

class DataQuelleForm(ModelForm):
    class Meta:
        model = DataQuelle
        fields = ['server','protocol','variable_address','variable_name']

class FileFieldForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
