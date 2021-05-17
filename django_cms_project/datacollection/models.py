from django.db import models

# Create your models here.

class DataQuelle(models.Model):
    server = models.CharField(max_length=100, default='localhost:8083')
    protokol = models.CharField(max_length=10, default='mqtt')
    variable_address = models.CharField(max_length=100, default='/test/sin')
    variable_name = models.CharField(max_length=100, default='strom')

    def __str__(self):
        return self.protokol
