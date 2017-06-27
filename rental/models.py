from django.db import models

# Create your models here.

class Test(models.Model):
    id=models.CharField(primary_key=True,max_length=30)
    sn=models.CharField(max_length=30)
    extra=models.CharField(max_length=10)
    class Meta:
        verbose_name=('test')

class Store(models.Model):
    Sid=models.AutoField(primary_key=True)
    Snumber=models.CharField(max_length=20)
    Sname=models.CharField(max_length=10)
    Saddress=models.CharField(max_length=50)
    Stel=models.CharField(max_length=13)
    Sstime=models.TimeField()
    Setime=models.TimeField()
    SExist=models.BooleanField()
    class Meta:
        verbose_name=('stores')

class Worker(models.Model):
    id=models.AutoField(primary_key=True)
    FSnumber=models.ForeignKey(Store,related_name='Snumber_foreign')
    Wname=models.CharField(max_length=10)
    Wtel=models.CharField(max_length=13,null=True)
    Wsecret=models.CharField(max_length=15)
    WIDnumber=models.CharField(max_length=18)
    Wtittle=models.CharField(max_length=10)
    class Meta:
        verbose_name=('workers')

class Cartype(models.Model):
    CTnumber=models.AutoField(primary_key=True)#车型编号，主码
    CTbrand=models.CharField(max_length=15) #车的类型
    CTprice=models.FloatField()     #基本价格
    CTcost=models.FloatField()      #押金
    CTseats=models.IntegerField()   #座位数
    CTengine=models.CharField(max_length=10)    #引擎号
    CTgears=models.BooleanField()   #是否为自动挡
    CTdrawway=models.CharField(max_length=15,null=True)   #图片路径
    CTaddtime=models.DateField()            #增加时间
    CTperson=models.ForeignKey(Worker,related_name='addPerson')
    class Meta:
        verbose_name=('cartypes')

class Car(models.Model):
    Cid=models.AutoField(primary_key=True)
    Cnumber=models.CharField(max_length=10)
    Clicense=models.CharField(max_length=10)        
    Cpurchase=models.DateField()
    Cseller=models.CharField(max_length=50)
    Csettime=models.DateField()
    Cuse=models.BooleanField()
    Wnumber=models.ForeignKey(Worker,related_name='addperson')
    CTnumber=models.ForeignKey(Cartype,related_name='typeofcar')
    class Meta:
        verbose_name=('cars')

class Order(models.Model):
    OrderNO=models.CharField(primary_key=True,max_length=20)
    DriverNO=models.CharField(max_length=18)
    Drivername=models.CharField(max_length=15,null=True)
    Completedate=models.DateField()
    Starttime=models.DateField()
    Preturntime=models.DateField()
    Freturntime=models.DateField()
    Finpay=models.FloatField()
    Conpay=models.FloatField(null=True)
    DamageDeposit=models.FloatField()
    RentDeposit=models.FloatField()
    IllegalDeposit=models.FloatField()
    DamageMoney=models.FloatField(null=True)
    IllegalMoney=models.FloatField(null=True)  
    OrderStatus=models.IntegerField()
    Wnumber=models.ForeignKey(Worker,related_name='worker')
    Cnumber=models.ForeignKey(Car,related_name='carnum')   
    class Meta:
        verbose_name=('orders')    
    
class ConRent(models.Model):
    ConID=models.AutoField(primary_key=True)
    ConStartTime=models.DateField()
    ConEndTime=models.DateField()
    CONpay=models.FloatField()
    OrderNO=models.ForeignKey(Order,related_name='ordernum')
    class Meta:
        verbose_name=('conrents')      

class Illegal(models.Model):
    IllID=models.AutoField(primary_key=True)
    IllegalTime=models.DateField()
    IllegalMoney=models.FloatField()   
    Detail=models.CharField(max_length=50)
    Cnumber=models.ForeignKey(Car,related_name='carNum')
    class Meta:
        verbose_name=('illegals')      