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
        verbose_name=('stores')

class Worker(models.Model):
    id=models.IntegerField(primary_key=True)
    FSnumber=models.ForeignKey(Store,related_name='Snumber_foreign')
    Wname=models.CharField(max_length=10)
    Wtel=models.CharField(max_length=13)
    Wsecret=models.CharField(max_length=15)
    WIDnumber=models.CharField(max_length=18)
    class Meta:
        verbose_name=('workers')