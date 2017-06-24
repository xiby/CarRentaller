from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from rental.models import Worker
from rental.models import Cartype
from rental.models import Car
from rental.models import Order
from rental.models import ConRent
from rental.models import Illegal

from datetime import datetime

from django.db import connection
# import models

def index(request):
    return render(request,'login.html')

#登陆函数
def login(request):
    if request.method=='GET':
        return render(request,'login.html')

    if request.method=='POST' and 'login' in request.POST:
        print('posting')
        userid=request.POST['userid']
        usertittle=request.POST['job']
        
        if Worker.objects.filter(id=userid,Wtittle=usertittle).exists():
            user=Worker.objects.get(id=userid,Wtittle=usertittle)
            if user.Wsecret==request.POST['password']:
                if usertittle=='职工':
                    response=redirect('/worker/')
                    return response
                elif usertittle=='经理':
                    return HttpResponse('经理界面')
                elif usertittle=='财务员':
                    return HttpResponse('财务员界面')
                else:
                    return HttpResponse('发生内部错误')
            else:
                return HttpResponse('密码错误')
        else:
            return HttpResponse('用户不存在')
    
    else:
        return HttpResponse('ERROR')

def findcars(datelist,cars):             #查询满足时间条件的车辆
    ans=list()
    for item in cars:
        if datelist[0]>item[8] or datelist[1]<item[7]:
            ans.append(item)
    return ans

def getCartypeInfo(brand,seats,gears,datelist):
    if gears=='0':
        gears=False
    else:
        gears=True
    cursor=connection.cursor()
    sql='''select Cnumber,CTbrand,CTseats,CTgears,CTprice,CTcost,CTdrawway,Starttime,Preturntime 
    from rental_car,rental_cartype,rental_order 
    where rental_car.CTnumber_id=rental_cartype.CTnumber 
    and rental_order.Cnumber_id=rental_car.Cid and rental_order.OrderStatus>1'''
    cursor.execute(sql)
    ans=cursor.fetchall()
    ans=findcars(datelist,ans)
    l=list()
    tmp=dict()
    for item in ans:
        tmp['Cnumber']=item[0]
        tmp['CTbrand']=item[1]
        tmp['CTseats']=item[2]
        tmp['CTgears']=item[3]
        tmp['CTprice']=item[4]
        tmp['CTcost']=item[5]
        tmp['CTdraway']=item[6]
        l.append(tmp)
    return l

def worker(request):
    if request.method=='GET':
        return render(request,'worker.html')
    elif request.method=='POST' and 'showtype' in request.POST:
        brand=request.POST['brand']
        seats=(request.POST['seats'])
        gears=request.POST['gears']
        timelist=list()
        timelist.append(datetime.strptime(request.POST['startdate'],'%Y-%m-%d').date())
        timelist.append(datetime.strptime(request.POST['enddate'],'%Y-%m-%d').date())
        ans=getCartypeInfo(brand,seats,gears,timelist)
        
        return render(request,'showcars.html',{"data":ans})
    else:
        return HttpResponse("ERROR")
        