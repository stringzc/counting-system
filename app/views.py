from django.shortcuts import render
from django.http import JsonResponse
from app.models import Person,Course,UandC,UandP,CandImg,QDI,DLI,BDI
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
    if data['ID'] == 'wx':
        username = data['username']
        if username.isdigit():
            user = Person.objects.filter(phone=username)
        else:
            user = Person.objects.filter(name=username)
        if user:
            user = user.first()
            password = data['password']
            power = UandP.objects.filter(cid=user.uid)[0]
            if check_password(password,user.password):
                ret = True
            else:
                ret = False
            if ret:
                DLI.objects.create(IP=str(user.name),uid=user.uid,times=datetime.now())
                return HttpResponse(json.dumps({"ret":"True","power":power.power}))
            else:
                return HttpResponse(json.dumps({"ret":"False"}))
        else:
            return HttpResponse(json.dumps({"ret":"False"}))

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
    if data['ID'] == "wx":
        username = data['username']
        user = Person.objects.filter(name=username)[0]
        classlist = UandC.objects.filter(uid=user.uid)
        alls = []
        for i in classlist:
            cls = Course.objects.filter(cid=i.cid)[0]
            keshi = CandImg.objects.filter(cid=i.cid)[0]
            alls.append({'class':cls.classs,'images':str(cls.img),'description':cls.description,'keshi':keshi.keshi,'times':i.times,'RC':i.RC,'id':str(int(i.uid)) + "+" + str(int(i.cid))})
        if len(alls) == 0:
            return HttpResponse(json.dumps({"ret":"2","classlist":alls},ensure_ascii=False,cls=ComplexEncoder))
        return HttpResponse(json.dumps({"ret":"0","classlist":alls},ensure_ascii=False,cls=ComplexEncoder))


def myclass(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        uid,cid =data['id'][0],data['id'][-1]
        Ju = UandC.objects.filter(Q(uid=uid)&Q(cid=cid)).first()
        Jc = Course.objects.filter(cid=cid).first()
        images = CandImg.objects.filter(cid=cid).first()
        imagelist=[{'urls':str(images.show1)},{'urls':str(images.show2)},{'urls':str(images.show3)},{'urls':str(images.show4)}]
        qdlist=[]
        for i in QDI.objects.filter(Q(uid=uid)&Q(cid=cid)):
            qdlist.append({"id":i.qid,"times":i.times})
        ret = len(qdlist) > 0
        alls = {'class':Jc.classs,'images':str(Jc.img),'descriptionall':Jc.descriptionall,'keshi':images.keshi,'times':Ju.times,'RC':Ju.RC,'imagelist':imagelist,'qdlist':qdlist,'ret':not ret}
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
    if data['ID'] == 'wx':
        uid,cid =data['id'][0],data['id'][-1]
        Ju = UandC.objects.filter(Q(uid=uid)&Q(cid=cid)).first()
        Ju.RC -= 1
        Ju.save()
        QDI.objects.create(uid=uid,cid=cid,times=datetime.now())
        return HttpResponse(json.dumps({"ret":"True"}))

def bdfind(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        name = data['values']
        if name.isdigit():
            stu = Person.objects.filter(phone=name)
        else:
            stu = Person.objects.filter(name=name)
        if stu:
            stu = stu.first()
            cls = UandC.objects.filter(uid=stu.uid)
            myclasslist = []
            for i in cls:
                if i.RC > 0:
                    C = Course.objects.filter(cid=i.cid).first()
                    myclasslist.append({"images":str(C.img),"class":C.classs,"description":C.description, "RC":i.RC, "id":str(stu.uid) + "+" + str(i.cid)})
            cls = Course.objects.all()
            classlist = []
            for i in cls:
                C = CandImg.objects.filter(cid=i.cid).first()
                classlist.append({"images":str(i.img),"class":i.classs,"description":i.description, "keshi":C.keshi, "id":str(stu.uid) + "+" + str(i.cid)})
            showmy = len(myclasslist) > 0
            showc = len(classlist) > 0
            return HttpResponse(json.dumps({"ret":True,"datas":{"values":name,"sname":stu.name,"sphone":stu.phone,"showmy":not showmy,"showc":not showc,"myclasslist":myclasslist,"classlist":classlist}}))
        else:
            return HttpResponse(json.dumps({"ret":False}))


def tuike(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        uid,cid = data['ids'][0],data['ids'][-1]
        cls = UandC.objects.filter(Q(uid=uid)&Q(cid=cid)).first()
        keshi = CandImg.objects.filter(cid=cid).first()
        if cls.RC >= keshi.keshi:
            cls.RC -= keshi.keshi
        else:
            cls.RC = 0
        cls.save()
        return HttpResponse(json.dumps({"ret":True}))


def bd(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        uid,cid = data['ids'][0],data['ids'][-1]
        cls = UandC.objects.filter(Q(uid=uid)&Q(cid=cid))
        ks = CandImg.objects.filter(cid=cid).first()
        BDI.objects.create(uid=uid,cid=cid,times=datetime.now())
        if cls:
            cls = cls.first()
            cls.RC += ks.keshi
            cls.save()
        else:
            UandC.objects.create(uid=uid,cid=cid,RC=ks.keshi,times=datetime.now())
        return HttpResponse(json.dumps({"ret":True}))

