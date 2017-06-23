from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render,redirect
from . import models

def index(request):
    return render(request,'login.html')

def login(request):
    # print(request.POST)
    for item in request.POST:
        print(item)
    if request.method=='GET':
        return render(request,'login.html')

    if request.method=='POST':
        username=request.POST['username']
        if request.POST['password']=='123' and 'worker'== request.POST['job']:
            return HttpResponse("log in success!")
        else:
            return HttpResponse("log in failed")
    
