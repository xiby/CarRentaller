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
from rental.models import Test

import datetime

from django.db import connection
cursor=connection.cursor()
# import models

def account(request):
    if request.method=='GET':
        return HttpResponse('Hello I am an account!')
    else:
        return HttpResponse('ERROR')