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
                    response.set_cookie("userid",userid)
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
    tmp=list()
    d=dict()
    for item in car:
        d[item[0]].append([item[7],item[8]])
    for item in d.keys():
        for val in d.value:
            if(datalist[0]<val[1] and datalist[0]>val[0]) or (datalist[1]<val[1] and datalist[1]>val[0]):
                break
        else:
            tmp.append(item)
    for item in car:
        for cnum in tmp:
            if(item[0]==cnum):
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

def loggout(request):
    response=redirect('/login/')
    response.delete_cookie('userid')
    return response

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
        # print(type(request.POST['startdate']))
        #先以字符串的格式存储到session中，然后需要用到的时候再转换成时间的格式
        request.session['startdate']=request.POST['startdate']
        request.session['enddate']=request.POST['enddate']
        ans=getCartypeInfo(brand,seats,gears,timelist)
        
        return render(request,'showcars.html',{"data":ans})
    elif request.method=='POST' and 'confirm' in request.POST:
        request.session['carNo']=request.POST['']
    else:
        return HttpResponse("ERROR")

def complete(request):
    if request.method=='GET':
        return render(request,'completeorder.html')
    elif request.method=='POST' and 'confirm' in request.POST:
        #此时根据cookie 以及session里面的内容来生成订单信息
        uid=request.COOKIES['userid']
        try:
            user=Worker.objects.get(id=userid)
            storeID=user.FSnumber_id
            orderID=''+storeID
            date_now=datetime.datetime.now()
            date_now_str=date_now.strftime('%Y%m%d')
            orderID=orderID+date_now_str
            sql='select count(OrderNO) from rental_order where Completedate='+"'"+date_now_str+"'"
            cursor=connection.cursor()
            cursor.execute(sql)
            ans=cursor.fetchall()
            orderID=orderID+str(ans[0]).zfill(4)
            #订单号填充完成
            driverName=request.POST['DName']
            driverNO=request.POST['DNo']
            startdate=request.session['startdate']
            enddate=request.session['endddate']
            #查询出该车的单价以及各种押金
            sql='select CTprice,CTcost from rental_car,rental_cartype where '

            #查询出

            

        except ObjectDoesNotExist:
            return HttpResponse('ERROR')

        