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

class Cartype(models.Model):
    CTnumber=models.CharField(primary_key=True,max_length=15)#车型编号，主码
    CTbrand=models.CharField(max_length=15) #车的类型
    CTprice=models.FloatField()     #基本价格
    CTcost=models.FloatField()      #押金
    CTseats=models.IntegerField()   #座位数
    CTengine=models.CharField(max_length=10)    #引擎号
    CTgears=models.BooleanField()   #是否为自动挡
    CTdrawway=models.CharField(max_length=15)   #图片路径
    CTaddtime=models.TimeField()            #增加时间
    CTperson=models.ForeignKey(Worker,related_name='addPerson')

# class Car(models.Model):
#     Cid=models.IntegerField(primary_key=True)
#     Cnumber=models.CharField(max_length=10)
#     Clicense=models.CharField(max_length=10)        #字段有何意义？
#     Cpurchase=models.DataField()
#     Cseller=models.CharField(max_length=50)
#     Csettime=models.DataField()
#     Csettime=models.DataField()
#     Cuse=models.BooleanField()
#     Wnumber=models.ForeignKey(Worker,related_name='addperson')