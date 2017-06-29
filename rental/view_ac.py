from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import json

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

def account(request):
    if request.method=='GET':
        return render(request,'account.html')
    elif request.method=='POST':
        if 'year' in request.POST:
            data=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            sql='select month(Freturntime),sum(Finpay)+sum(Conpay) from rental_order where year(Freturntime)=year(date_sub(now(),interval 1 year))'
            cursor.execute(sql)
            ans=cursor.fetchall()
            print(ans)
            for item in ans:
                data[int(item[0])-1]=float(item[1])
            return render_to_response('line.html',{"data":data})
        else:
            return render(request,'account.html')
    else:
        return HttpResponse('ERROR')