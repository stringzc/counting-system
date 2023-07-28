from django.shortcuts import render
from django.http import JsonResponse
from app.models import Person,Course,UandC,UandP
import json
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
# Create your views here.

def weixinlogin(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = Person.objects.filter(name=username)[0]
    power = UandP.objects.filter(cid=user.uid)[0]
    print(check_password(password,user.password))
    if check_password(password,user.password):
        ret = 'True'
    else:
        ret = 'False'
    return HttpResponse(json.dumps({"ret":ret,"power":power.power}))

def changePassword(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = Person.objects.filter(name=username)[0]
    user.password = make_password(password)
    user.save()
    ret = 'True'
    return HttpResponse(json.dumps(ret))

