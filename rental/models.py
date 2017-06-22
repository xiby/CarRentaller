from django.db import models

# Create your models here.

class Test(models.Model):
    id=models.CharField(primary_key=True,max_length=30)
    sn=models.CharField(max_length=30)
    extra=models.CharField(max_length=10)
    class Meta:
        verbose_name=('test')

class Store(models.Model):
    Snumber=models.CharField(primary_key=True,max_length=20)
    Sname=models.CharField(max_length=10)
    Saddress=models.CharField(max_length=50)
    Stel=models.CharField(max_length=13)
    Sstime=models.TimeField()
    Setime=models.TimeField()
    SExist=models.BooleanField()
    class Meta:
        verbose_name=('test')