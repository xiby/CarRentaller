
'''
可能的解决方法：先查询，然后在完成订单时输入查询到的车辆编号
                在续租的时候也可以采用该处理方法
'''

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render,redirect,render_to_response
from django.core.exceptions import ObjectDoesNotExist
from rental.models import Worker
from rental.models import Cartype
from rental.models import Car
from rental.models import Order
from rental.models import ConRent
from rental.models import Illegal
from rental.models import Test

import datetime

from django.db import connection
cursor=connection.cursor()
# import models
status={0:'待取车',1:'进行中',2:'待验收',4:'已完成'}
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
        print(userid)
        print(usertittle)
        if Worker.objects.filter(id=userid,Wtittle=usertittle,WExit=1).exists():
            user=Worker.objects.get(id=userid,Wtittle=usertittle)
            if user.Wsecret==request.POST['password']:
                if usertittle=='职工':
                    response=redirect('/worker/')
                    response.set_cookie("userid",userid)
                    return response
                elif usertittle=='经理':
                    response=redirect('/manager/')
                    response.set_cookie('userid',userid)
                    return response
                elif usertittle=='财务员':
                    response=redirect('/account/')
                    response.set_cookie('userid',userid)
                    return response
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
    for item in cars:
        if item[0] not in d.keys():
            d[item[0]]=list()
        d[item[0]].append(list([item[7],item[8]]))
    for item in d.keys():
        for val in d[item]:
            if(datelist[0]<val[1] and datelist[0]>val[0]) or (datelist[1]<val[1] and datelist[1]>val[0]):
                break
        else:
            tmp.append(item)
    for item in cars:
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
    sql='''select distinct Cnumber,CTbrand,CTseats,CTgears,CTprice,CTcost,CTdrawway,Starttime,Preturntime,Cid 
    from rental_car,rental_cartype,rental_order 
    where rental_car.CTnumber_id=rental_cartype.CTnumber 
    and rental_order.Cnumber_id=rental_car.Cid'''
    cursor.execute(sql)
    ans=cursor.fetchall()
    print(ans)
    ans=findcars(datelist,ans)
    l=list()
    for item in ans:
        tmp=dict()
        tmp['Cnumber']=item[0]
        tmp['CTbrand']=item[1]
        tmp['CTseats']=item[2]
        tmp['CTgears']=item[3]
        tmp['CTprice']=item[4]
        tmp['CTcost']=item[5]
        tmp['CTdraway']=item[6]
        tmp['cid']=item[9]
        tmp['starttime']=item[7]
        tmp['preturntime']=item[8]
        l.append(tmp)
    print(l)
    return l

def logout(request):
    response=render_to_response('success.html',{"data":'/login/'})
    response.delete_cookie('userid')
    return response

def worker(request):
    if request.method=='POST':
        for item in request.POST:
            print(item)
    if request.method=='GET':
        return render(request,'worker.html')
    elif request.method=='POST' and 'showtype' in request.POST:
        brand=request.POST['brand']
        seats=(request.POST['seats'])
        gears=request.POST['gears']
        timelist=list()
        timelist.append(datetime.datetime.strptime(request.POST['startdate'],'%Y-%m-%d').date())
        timelist.append(datetime.datetime.strptime(request.POST['enddate'],'%Y-%m-%d').date())
        # print(type(request.POST['startdate']))
        #先以字符串的格式存储到session中，然后需要用到的时候再转换成时间的格式
        request.session['startdate']=request.POST['startdate']
        request.session['enddate']=request.POST['enddate']
        ans=getCartypeInfo(brand,seats,gears,timelist)
        return render(request,'showcars.html',{"data":ans})
    elif request.method=='POST' and 'confirm' in request.POST:
        print('hehe')
        return redirect('/generate/')
    else:
        return HttpResponse("ERROR")

def complete(request):
    if request.method=='GET':
        return render(request,'completeorder.html')
    elif request.method=='POST' and 'confirm' in request.POST:
        #此时根据cookie 以及session里面的内容来生成订单信息
        userid=request.COOKIES['userid']
        try:
            user=Worker.objects.get(id=userid)
            storeID=user.FSnumber_id
            orderID=''+str(storeID).zfill(5)
            date_now=datetime.datetime.now()
            date_now_str=date_now.strftime('%Y%m%d')
            orderID=orderID+date_now_str
            sql='select count(OrderNO) from rental_order where Completedate='+"'"+date_now_str+"'"
            cursor=connection.cursor()
            cursor.execute(sql)
            ans=cursor.fetchall()
            orderID=orderID+str(ans[0][0]+1).zfill(4)
            #订单号填充完成
            driverName=request.POST['DName']
            driverNO=request.POST['DNo']
            startdate=datetime.datetime.strptime(request.session['startdate'],'%Y-%m-%d')
            enddate=datetime.datetime.strptime(request.session['enddate'],'%Y-%m-%d')
            completedate=date_now.date()
            cid=request.POST['carid']
            #查询出该车的单价以及各种押金
            print(cid)
            sql='''select CTprice,CTcost from rental_car,rental_cartype 
            where rental_car.CTnumber_id=rental_cartype.CTnumber and rental_car.Cid='''+cid
            cursor.execute(sql)
            ans=cursor.fetchall()
            print(ans)
            price=ans[0][0]     #日租金
            pay=price*(enddate-startdate).days
            deposit=ans[0][1]   #押金
            state=0
            damagedeposit=1000
            rentdeposit=1000
            illegaldeposit=1000
            damagemonet=0
            illegalmoney=0
            # sql='insert into rental_order values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            neworder=Order(orderID,
            driverNO,
            driverName,
            completedate,
            startdate,
            enddate,
            enddate,
            pay,
            0,
            damagedeposit,
            rentdeposit,
            illegaldeposit,
            0,0,0,
            userid,cid)
            neworder.save()
            return render(request,'success.html',{'data':'/worker/'})
        except ObjectDoesNotExist:
            return HttpResponse('ERROR')
def showAOrders(request):
    if request.method=='GET':
        sql='''select * from rental_order
        where OrderStatus=0 and Cnumber_id='''+str(request.COOKIES['userid'])
        cursor.execute(sql)
        ans=cursor.fetchall()
        # print(ans)
        #查询出所有的预约单
        data=list()
        for item in ans:
            tmp=dict()
            tmp['OrderNO']=item[0]
            tmp['cid']=item[13]
            tmp['Drivername']=item[15]
            tmp['completedate']=item[16].strftime('%Y-%m-%d')
            print(tmp['completedate'])
            data.append(tmp)
        return render(request,'showAOrders.html',{"data":data})
    elif request.method=='POST' and 'delete' in request.POST:
        orderid=request.POST['Cancelorderid']
        try:
            Order.objects.get(OrderNO=orderid).delete()
            return render(request,'success.html',{'data':'/show/'})
        except ObjectDoesNotExist:
            return HttpResponse("该订单号不存在")
    elif request.method=='POST' and 'confirm' in request.POST:
        orderid=request.POST['Confirmorderid']
        try:
            order=Order.objects.get(OrderNO=orderid)
            order.OrderStatus=1
            order.save()
            return render(request,'success.html',{'data':'/show/'})
        except ObjectDoesNotExist:
            return HttpResponse('该订单号不存在')

def doConRent(orderID,interval):
    Now=datetime.datetime.now().date()
    End=Now+datetime.timedelta(days=interval)
    Now_str=Now.strftime('%Y-%m-%d')
    End_str=End.strftime('%Y-%m-%d')
    try:
        order=Order.objects.get(OrderNO=orderID)
        car=Car.objects.get(Cid=order.Cnumber.Cid)
        cartype=Cartype.objects.get(CTnumber=car.CTnumber.CTnumber)
        price=cartype.CTprice
        pay=price*interval
        order.Conpay=order.Conpay+pay
        newConrent=ConRent(ConStartTime=order.Preturntime,ConEndTime=End,CONpay=pay,OrderNO=order)
        order.save()
        newConrent.save()
        return True
    except ObjectDoesNotExist:
        return False

def showRunning(request):
    if request.method=='GET':
        sql='''select * from rental_order
        where OrderStatus=1 and Cnumber_id='''+str(request.COOKIES['userid']) 
        cursor.execute(sql)
        ans=cursor.fetchall()
        data=list()
        for item in ans:
            tmp=dict()
            tmp['OrderNO']=item[0]
            tmp['cid']=item[13]
            tmp['Drivername']=item[15]
            tmp['completedate']=item[16].strftime('%Y-%m-%d')
            tmp['prereturndate']=item[3].strftime('%Y-%m-%d')
            tmp['status']=status[item[12]]
            print(tmp['completedate'])
            data.append(tmp)
        return render(request,'showRunning.html',{'data':data})
    elif request.method=='POST':
        if 'conrent' in request.POST:
            # days=int(request.POST['days'])            ##########
            days=7
            orderID=request.POST['orderNO']
            if doConRent(orderID,days):
                return render(request,'success.html',{"data":'/showRunning/'})
            else:
                return HttpResponse('ERROR')
        elif 'Back' in request.POST:
            orderNO=request.POST['BackOrderNO']
            try:
                order=Order.objects.get(OrderNO=orderNO)
                now=datetime.datetime.now().date()
                if order.OrderStatus==1:
                    order.OrderStatus=2
                    order.Freturntime=now
                    order.save()
                    return render(request,'success.html',{'data':'/showRunning/'})
                else:
                    return HttpResponse('请检查输入订单号的状态')
            except ObjectDoesNotExist:
                return HttpResponse("该订单不存在")
        else:
            return HttpResponse("ERROR!")
    else:
        return HttpResponse("ERROR")
def checkillegal(cid,starttime,Freturntime):
    return_time_str=datetime.datetime.strftime(Freturntime,'%Y-%m-%d')
    start_time_str=datetime.datetime.strftime(starttime,'%Y-%m-%d')
    sql='''select IllID,sum(IllegalMoney) from rental_illegal
    where Cnumber_id='''+cid+' and IllegalTime<'+return_time_str+' and '+'IllegalTime>'+start_time_str+' and processed=0'
    cursor.execute(sql)
    ans=cursor.fetchall()
    if len(ans)!=0:
        sql='update rental_illegal set processed=1 where IllID='+ans[0][0]+' and processed=0'
        return ans[0][1]
    else:
        return 0
def getWaitting(userid):
    sql='''select * from rental_order
    where OrderStatus=2 and Cnumber_id='''+userid
    cursor.execute(sql)
    ans=cursor.fetchall()
    data=list()
    for item in ans:
        tmp=dict()
        tmp['OrderNO']=item[0]
        tmp['cid']=item[13]
        tmp['Drivername']=item[15]
        tmp['completedate']=item[16].strftime('%Y-%m-%d')
        tmp['frereturndate']=item[4].strftime('%Y-%m-%d')
        tmp['status']=status[item[12]]
        print(tmp['completedate'])
        data.append(tmp)
    return data
def showWaitting(request):
    if request.method=='GET':
        return render(request,'showWaitting.html',{"data":getWaitting(request.COOKIES['userid'])})
    elif request.method=='POST':
        if 'confirm' in request.POST:
            orderID=str(request.POST['orderID'])
            print(type(orderID),orderID)
            try:
                tmporder=Order.objects.get(OrderNO=orderID,OrderStatus=2)
                tmporder.OrderStatus=3
                tmporder.save()
                return render(request,'success.html',{"data":'/showWaitting/'})
            except ObjectDoesNotExist:
                return HttpResponse("请检查订单号")
    else:
        return HttpResponse('ERROR')

def getFinished(userid):
    sql='select * from rental_order where OrderStatus=3 and Wnumber_id='+userid
    cursor.execute(sql)
    ans=cursor.fetchall()
    data=list()
    for item in ans:
        tmp=dict()
        tmp['orderID']=item[0]
        tmp['DriverNO']=item[1]
        tmp['Drivername']=item[15]
        tmp['Finpay']=item[5]
        tmp['Conpay']=item[6]
        tmp['DamageDeposit']=item[7]
        tmp['RentDeposit']=item[8]
        tmp['IllegalDeposit']=item[9]
        tmp['DamageMoney']=item[10]
        tmp['IllegalMoney']=item[11]
        tmp['Cid']=item[13]
        tmp['completedate']=item[16]
        tmp['returndate']=item[4]
        data.append(tmp)
    return data
def showFinished(request):
    if request.method=='GET':
        data=getFinished(request.COOKIES['userid'])
        return render(request,'showFinished.html',{'data':data})
    else:
        return HttpResponse('Hello')
def fetchCar(orderID):
    sql='''update rental_order
    set OrderState=1
    where OrderNO='''+"'"+orderID+"'"
    cursor.execute(sql)
    cursor.commit()

def returnCar(orderID):
    sql='''update rental_order
    set OrderState=2
    where OrderNO='''+"'"+orderID+"'"
    cursor.execute(sql)
    cursor.commit()

def finish(orderID):
    sql='''update rental_order
    set OrderState=3
    where OrderNO='''+"'"+orderID+"'"
    cursor.execute(sql)
    cursor.commit()