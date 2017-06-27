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

def manager(request):
    if request.method=='GET':
        try:
            worker=Worker.objects.get(id=request.COOKIES['userid'])
            return render(request,'manager.html',{"data":worker.Wname})
        except ObjectDoesNotExist:
            return HttpResponse("ERROR")
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


def workerm(request):
    if request.method=='GET':
        return render(request,'workerm.html')
