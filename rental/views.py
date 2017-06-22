from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render
from . import models

def index(request):
    M=models.Test("789","456","741")
    M.save()
    M=models.test.objects.all()
    for item in M:
        print(item.id,item.sn,item.extra)
    return render(request,'login.html')