from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DataQuelle(models.Model):
    server = models.CharField(max_length=100,default='')
    protocol = models.CharField(max_length=10,default='')
    variable_address = models.CharField(max_length=100,)
    variable_name = models.CharField(max_length=100)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.server
