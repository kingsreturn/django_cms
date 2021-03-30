from django.db import models

# Create your models here.
class TimebasedData(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    typ = models.CharField(max_length=60)