from django.shortcuts import render
from django.http import JsonResponse
from app.models import Person,Course,UandC,UandP,CandImg
import json
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
# Create your views here.
from datetime import date, datetime
from django.db.models import Q
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def index(request):
    return render(request,'index.html')
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

def getclass(request):
    data = json.loads(request.body)
    username = data['username']
    user = Person.objects.filter(name=username)[0]
    classlist = UandC.objects.filter(uid=user.uid)
    alls = []
    for i in classlist:
        cls = Course.objects.filter(cid=i.cid)[0]
        keshi = CandImg.objects.filter(cid=i.cid)[0]
        alls.append({'class':cls.classs,'images':str(cls.img),'description':cls.description,'keshi':keshi.keshi,'times':i.times,'RC':i.RC,'id':str(int(i.uid)) + "+" + str(int(i.cid))})
    print(classlist)
    return HttpResponse(json.dumps(alls,ensure_ascii=False,cls=ComplexEncoder))


def myclass(request):
    data = json.loads(request.body)
    uid,cid =data['id'][0],data['id'][-1]
    Ju = UandC.objects.filter(Q(uid=uid)&Q(cid=cid)).first()
    print(Ju.uid,Ju.cid)
    Jc = Course.objects.filter(cid=cid).first()
    images = CandImg.objects.filter(cid=cid).first()
    imagelist=[{'urls':str(images.show1)},{'urls':str(images.show2)},{'urls':str(images.show3)},{'urls':str(images.show4)}]
    alls = {'class':Jc.classs,'images':str(Jc.img),'descriptionall':Jc.descriptionall,'keshi':images.keshi,'times':Ju.times,'RC':Ju.RC,'imagelist':imagelist}
    return HttpResponse(json.dumps(alls,cls=ComplexEncoder))


def findQD(request):
    data = json.loads(request.body)
    name = data['values']
    if name.isdigit():
        stu = Person.objects.filter(phone=name)
    else:
        stu = Person.objects.filter(name=name)
    if stu:
        stu = stu.first()
        cls = UandC.objects.filter(uid=stu.uid)
        clslist = []
        if cls:
            for i in cls:
                if i.RC >= 1:
                    s = Course.objects.filter(cid=i.cid).first()
                    clslist.append({'class':s.classs,'images':str(s.img),'description':s.description,'RC':i.RC,'id':str(i.uid) + '+' + str(i.cid)})

        else:
            return HttpResponse(json.dumps({"ret":"F2","sphone":stu.phone,"sname":stu.name},cls=ComplexEncoder))

        if clslist:
            return HttpResponse(json.dumps({"ret":"F1","sphone":stu.phone,"sname":stu.name,"classlist":clslist}))
        else:
            return HttpResponse(json.dumps({"ret":"F2","sphone":stu.phone,"sname":stu.name}))

    else:
        return HttpResponse(json.dumps({"ret":"False"}))


def QD(request):
    data = json.loads(request.body)
    uid,cid =data['id'][0],data['id'][-1]
    print(uid,cid)

    Ju = UandC.objects.filter(Q(uid=uid)&Q(cid=cid)).first()
    print(Ju.cid)
    Ju.RC -= 1
    Ju.save()
    
    return HttpResponse(json.dumps({"ret":"True"}))


