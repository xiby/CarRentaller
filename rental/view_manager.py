from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render,redirect,render_to_response
from django.core.exceptions import ObjectDoesNotExist
from rental.models import Store
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

def logout(request):
    response=redirect('/login/')
    response.delete_cookie('userid')
    return response

def manager(request):
    if request.method=='GET':
        try:
            worker=Worker.objects.get(id=request.COOKIES['userid'])
            return render(request,'manager.html',{"data":worker.Wname})
        except ObjectDoesNotExist:
            return HttpResponse("ERROR")
    elif request.method=='POST' and 'logout' in request.POST:
        return logout(request)
    else:
        return HttpResponse('ERROR')

def addworker(request):
    if request.method=='GET':
        return render(request,'addworker.html')
    if request.method=='POST':
        if 'addworker' in request.POST:
            for item in request.POST:
                if len(request.POST[item])==0:
                    print('ERROR')
                    return HttpResponse('属性列不能为空')
            # Snumber=int(request.POST['snumber'])
            wname=request.POST['wname']
            wtel=request.POST['wtel']
            sn=request.POST['wpasw']
            widnum=request.POST['widnum']
            try:
                workerNow=Worker.objects.get(id=int(request.COOKIES['userid']))
                snumber=workerNow.FSnumber.Sid
                store=Store.objects.get(Sid=snumber)
                newworker=Worker(FSnumber=store,Wname=wname,Wtel=wtel,Wsecret=sn,
                WIDnumber=widnum,Wtittle='职工',WExit=1)
                newworker.save()
                return render(request,'success.html',{"data":'/manager/'})
            except ObjectDoesNotExist:
                return HttpResponse('无法查询到该门店')

def dropworker(request):
    if request.method=='GET':
        return render_to_response('dropworker.html')

    elif request.method=='POST':
        if 'confirm' in request.POST:
            userid=request.POST['wid']
            username=request.POST['wname']
            try:
                tmp=Worker.objects.get(id=userid,Wname=username)
                if tmp.WExit==1:
                    tmp.WExit=0
                    tmp.save()
                    return render(request,'success.html',{"data":'/manager/'})
                else:
                    return HttpResponse('该用户不存在')
            except ObjectDoesNotExist:
                return HttpResponse('输入了无效的信息')

def addCar(request):
    if request.method=='GET':
        ct=Cartype.objects.all()
        ans=list()
        for item in ct:
            ans.append(item.CTnumber)
        return render_to_response('addCar.html',{"data":ans})
    if request.method=='POST':
        if 'confirm' in request.POST:
            try:
                ctnumber=request.POST['choice']
                cnumber=request.POST['carid']
                clicense=request.POST['clicense']
                cseller=request.POST['cseller']
                pdate=request.POST['pdate']
                pdate=datetime.datetime.strptime(pdate,'%Y-%m-%d').date()
                type=Cartype.objects.get(CTnumber=ctnumber)
                date_now=datetime.datetime.now().date()
                userNow=Worker.objects.get(id=int(request.COOKIES['userid']))
                newcar=Car(Cnumber=cnumber,Clicense=clicense,
                Cpurchase=pdate,Cseller=cseller,Csettime=date_now,
                Cuse=1,Wnumber=userNow,CTnumber=type)
                newcar.save()
                return render_to_response('success.html',{"data":'/manager/'})
            except ObjectDoesNotExist:
                return HttpResponse('发生内部错误')

def dropCar(request):
    if request.method=='GET':
        cars=Car.objects.filter(Cuse=1)
        # print(locals())
        return render_to_response('dropCar.html',locals())
    if request.method=='POST':
        if 'confirm' in request.POST:
            carid=request.POST['cid']
            try:
                tmp=Car.objects.get(Cid=carid)
                tmp.Cuse=0
                tmp.save()
                return render_to_response('success.html',{"data":'/manager/'})
            except ObjectDoesNotExist:
                return HttpResponse('发生内部错误')
        else:
            return HttpResponse('发生了一些意料之外的错误')
    else:
        return HttpResponse('发生了一些意料之外的错误')
def showAll(request):
    if request.method=='GET':
        data=list()
        userid=request.COOKIES['userid']
        try:
            userNow=Worker.objects.get(id=userid)
            userStore=userNow.FSnumber
            ans=Worker.objects.filter(FSnumber=userStore,WExit=1)
            for item in ans:
                tmp=dict()
                tmp['id']=item.id
                tmp['wname']=item.Wname
                tmp['wtel']=item.Wtel
                tmp['widnumber']=item.WIDnumber
                tmp['wtittle']=item.Wtittle
                data.append(tmp)
            return render(request,'showWorkers.html',{"data":data})
        except ObjectDoesNotExist:
            return HttpResponse("发生内部错误")

def ctmanager(request):
    if request.method=='GET':
        cartype=Cartype.objects.all()
        return render_to_response('ctmanager.html',locals())
    elif request.method=='POST':
        if 'confirm' in request.POST:       #修改信息确认
            ctid=request.POST['ctid']
            if(ctid==''):
                return HttpResponse('编号列不能为空')
            else:
                try:
                    ctype=Cartype.objects.get(CTnumber=int(ctid))
                    newprice=request.POST['price']
                    newdeposit=request.POST['deposit']
                    if newprice!='':
                        ctype.CTprice=newprice
                    if newdeposit!='':
                        ctype.CTcost=newdeposit
                    ctype.save()
                    return render_to_response('success.html',{"data":'/'})
                except ObjectDoesNotExist:
                    return HttpResponse('输入了错误的车型编号')
                    
        elif 'addconfig' in request.POST:   #增加信息确认
            for item in request.POST:
                if request.POST[item]=='':
                    return HttpResponse('表单未填写完成，请返回上一界面重新填写！')
            else:
                try:
                    brand=request.POST['brand']
                    price=request.POST['price']
                    deposit=request.POST['deposit']
                    engine=request.POST['engine']
                    gears=request.POST['gears']
                    seats=request.POST['seats']
                    cartype=Cartype(CTbrand=brand,
                    CTprice=price,
                    CTcost=deposit,
                    CTseats=seats,
                    CTengine=engine,
                    CTgears=gears,
                    CTdrawway='./',
                    CTaddtime=datetime.datetime.now().date(),
                    CTperson=Worker.objects.get(id=int(request.COOKIES['userid'])))
                    cartype.save()
                    return render_to_response('success.html',{"data":'/'})
                except ObjectDoesNotExist:
                    return HttpResponse('发生了一个内部错误')
    else:
        return HttpResponse("发生了一个严重的错误，服务器收到了攻击")
def workerm(request):
    if request.method=='GET':
        return render(request,'workerm.html')