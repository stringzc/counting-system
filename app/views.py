from django.shortcuts import render
from django.http import JsonResponse
from app.models import Person
# Create your views here.

def weixinlogin(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = Person.objects.filter(username=username)[0]
    print(check_password(password,user.password))
    if check_password(password,user.password):
        ret = 'True'
    else:
        ret = 'False'
    return HttpResponse(json.dumps(ret))

