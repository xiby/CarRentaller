from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from rental.models import Worker
# import models

def index(request):
    return render(request,'login.html')

def login(request):
    if request.method=='GET':
        return render(request,'login.html')

    if request.method=='POST' and 'login' in request.POST:
        print('posting')
        userid=request.POST['userid']
        usertittle=request.POST['job']
        # usersn=Worker.objects.get(id=userid).objects().values('Wsecret')
        # sql='select Wsecret from rental_worker where id='+str(userid)
        # usersn=request.POST['password']
        
        # print(usersn)
        # if user==request.POST['password']:
        #     return HttpResponse('登陆成功')
        # else:
        #     return HttpResponse('密码输入错误')
        if Worker.objects.filter(id=userid,Wtittle=usertittle).exists():
            user=Worker.objects.get(id=userid,Wtittle=usertittle)
            if user.Wsecret==request.POST['password']:
                return HttpResponse('登陆成功')
            else:
                return HttpResponse('密码错误')
        else:
            return HttpResponse('用户不存在')