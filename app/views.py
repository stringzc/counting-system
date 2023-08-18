from django.shortcuts import render
from django.http import JsonResponse
from app.models import Person,Course,UandC,UandP,CandImg,QDI,DLI,BDI,UCI,plun,black,BASIC
import json
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
# Create your views here.
from datetime import date, datetime,timedelta
from django.db.models import Q
from PIL import Image
from django.core.files import File
import random
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def getcolor(a):
    color = ['BurlyWood', 'CadetBlue', 'Coral', 'Darkorange', 'DeepPink', 'IndianRed',  'Khaki', 'LightCoral', 'LightPink' ,'LightSalmon', 'Orange', 'OrangeRed', 'Orchid', 'PeachPuff', 'LightCyan']
    return color[a%(len(color))]


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
                return HttpResponse(json.dumps({"ret":"True","power":power.power,"username":user.name}))
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
        idss = 1
        for i in QDI.objects.filter(Q(uid=uid)&Q(cid=cid))[::-1]:
            qdlist.append({"id":idss,"times":i.times})
            idss += 1
        ret = len(qdlist) > 0
        alls = {'class':Jc.classs,'images':str(Jc.img),'descriptionall':Jc.descriptionall,'keshi':images.keshi,'times':Ju.times,'RC':Ju.RC,'imagelist':imagelist,'qdlist':qdlist,'ret':not ret}
        return HttpResponse(json.dumps(alls,cls=ComplexEncoder))


def check(tday,olds,nums):
    t = tday.split()
    o = olds.split()
    for i in range(len(t[0])):
        if t[0][i] == '-':
            continue
        if t[0][i] > o[0][i]:
            return True

    tall = list(map(float,t[1].split(":")))
    tall = tall[0]*3600 + tall[1]*60 + tall[2]
    oall = list(map(float,o[1].split(":")))
    oall = oall[0]*3600 + oall[1]*60 + oall[2]

    return tall > (oall + nums)

def checkDAY(tday,olds):
    t = tday.split()
    o = olds.split()
    for i in range(len(t[0])):
        if t[0][i] == '-':
            continue
        if t[0][i] > o[0][i]:
            return True
    return False



def findQD(request):
    data = json.loads(request.body)
    if data['ID'] == "wx":
        name = data['values']
        if name.isdigit():
            stu = Person.objects.filter(phone=name)
        else:
            stu = Person.objects.filter(name=name)
        if stu:
            stu = stu.first()
            allQDI = QDI.objects.all().order_by('-pk')
            qdlist = []
            times1 = str(datetime.now())
            if allQDI:
                for i in allQDI:
                    if not checkDAY(times1,str(i.times)):
                        name = Person.objects.get(uid=i.uid)
                        qdlist.append({"name":name.name,"times":i.times})
            cls = UandC.objects.filter(uid=stu.uid)
            clslist = []
            if cls:
                for i in cls:
                    qdis = QDI.objects.filter(Q(uid=stu.uid)&Q(cid=i.cid))
                    if qdis:
                        qids = max([int(j.qid) for j in qdis])
                        times2 = str(QDI.objects.get(qid=qids).times)
                        cooldown = BASIC.objects.all().first().Checkincooldown
                        ishow = check(times1,times2,cooldown)
                    else:
                        ishow = True

                    if i.RC >= 1:
                        s = Course.objects.filter(cid=i.cid).first()
                        clslist.append({'class':s.classs,'images':str(s.img),'description':s.description,'RC':i.RC,'id':str(i.uid) + '+' + str(i.cid), "ishow":ishow})
            else:
                return HttpResponse(json.dumps({"ret":"F2","sphone":stu.phone,"sname":stu.name},cls=ComplexEncoder))
            if clslist:
                return HttpResponse(json.dumps({"ret":"F1","sphone":stu.phone,"sname":stu.name,"classlist":clslist,"qdlist":qdlist},cls=ComplexEncoder))
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

def get_max_uid():
    return max([int(i['uid']) for i in Person.objects.all().values('uid')])

def weixinregistered(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        name = data['username']
        if Person.objects.filter(name=name):
            return HttpResponse(json.dumps({"ret":"F2"}))
        phone = data['userphone']
        if Person.objects.filter(phone=phone):
            return HttpResponse(json.dumps({"ret":"F3"}))
        password =make_password(data['password'])
        power = data['power']
        image_path = r"/work/counting-system/static/img/4.jpg"
        img_file = Image.open(image_path)
        img_file = File(img_file)
        uid = get_max_uid()
        Person.objects.create(uid= uid+1,name=name,phone=phone,password=password,img=img_file)
        UandP.objects.create(cid=uid+1,power=power+1)
        UCI.objects.create(uid=uid+1,times=datetime.now())
        return HttpResponse(json.dumps({"ret":"F1"}))



def logs(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        qdis = []
        for i in QDI.objects.all().order_by('-pk'):
            name = Person.objects.get(uid=i.uid)
            cls = Course.objects.get(cid=i.cid)
            qdis.append({"name":name.name,"class":cls.classs,"times":i.times})
        dlis = []
        for i in DLI.objects.all().order_by('-pk'):
            name = Person.objects.get(uid=i.uid)
            dlis.append({"name":name.name,"phone":i.IP,"times":i.times})
        bdis = []
        for i in BDI.objects.all().order_by('-pk'):
            nm = Person.objects.filter(uid=i.uid).first()
            cls = Course.objects.filter(cid=i.cid).first()
            bdis.append({"name":nm.name,"class":cls.classs,"times":i.times})
        return HttpResponse(json.dumps({"lists":{"qdlist":qdis,"dllist":dlis,"bdlist":bdis}},cls=ComplexEncoder))

def pluns(request):
    data = json.loads(request.body)
    if data['ID'] == "wx":
        nowtime = str(datetime.now())
        username = data['username']
        person = Person.objects.filter(name=username)
        if person:
            uid=person[0].uid
            plunsall = plun.objects.filter(uid=uid).order_by('-pk')
            quicks = False
            if plunsall:
                maxtimes = str(plunsall[0].times)
                cooldown = BASIC.objects.all().first().Commentonthecooldown
                if not check(nowtime,maxtimes,cooldown):
                    quicks = True
            if quicks:
                return HttpResponse(json.dumps({"ret":"F1"}))
            title = data['title']
            content = data['content']
            plun.objects.create(uid=uid,title=title,content=content,times=nowtime)
            return HttpResponse(json.dumps({"ret":"True"}))
        else:
            return HttpResponse(json.dumps({"ret":"F2"}))

def gethots(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        today = datetime.now()
        dlall = DLI.objects.all()
        dldict = {}
        for i in dlall:
            if i.times.year == today.year and i.times.month == today.month:
                if i.uid not in dldict.keys():
                    dldict[i.uid] = 1
                else:
                    dldict[i.uid] += 1
        users = len(dldict.keys())
        startday = BASIC.objects.all().first().STARTTIME
        d = timedelta(days=1)
        days = 0
        while startday < today:
            startday += d
            days += 1
        clist = []
        BDIall = BDI.objects.all()
        clsall = Course.objects.all()
        for i in clsall:
            clist.append([0,i.classs,getcolor(random.choice(list(range(31415926))))])
        guodu = {}
        for i in BDIall:
            nm = Course.objects.get(cid=i.cid).classs
            if nm not in guodu.keys():
                guodu[nm] = 1
            else:
                guodu[nm] += 1
        for i in range(len(clist)):
            if clist[i][1] in guodu.keys():
                clist[i][0] = guodu[clist[i][1]]
        clist.sort(reverse=True)
        for i in range(len(clist)):
            if i == 0:
                clist[0].append("static/hf3.png")
            else:
                if clist[i][0] != 0:
                    clist[i].append("static/hf2.png")
                else:
                    clist[i].append("static/hf1.png")
        maxs = clist[0][0]
        clist = [{'name':i[1],'color':i[2],'width':str(int(60*(i[0]/maxs))) + '%','url':i[3]} for i in clist]
        return HttpResponse(json.dumps({"days":days,"users":users,'Hots':clist}))


def getallcls(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        clsall = Course.objects.all()
        clslist = [{"id":"11","name":"admins","color":getcolor(random.choice(list(range(31415926)))),"url":"static/alladmins.png"}]
        clslist.append({"id":"10","name":"alluser","color":getcolor(random.choice(list(range(31415926)))),"url":"static/alluser.png"})
        for i in clsall:
            clslist.append({"id":i.cid,"name":i.classs,"color":getcolor(random.choice(list(range(31415926)))),"url":str(i.img)})

        return HttpResponse(json.dumps({"clslist":clslist}))


def getuserdate(request):
    data = json.loads(request.body)
    if data['ID'] == 'wx':
        id = data['id']
        datelist = []
        if id == "11":
            userall = UandP.objects.filter(Q(power=4)|Q(power=5))
            for i in userall:
                nm = Person.objects.get(uid=i.cid).name
                datelist.append({'id':i.cid,'name':nm,'checked':False})
        elif id == "10":
            userall = Person.objects.all()
            for i in userall:
                datelist.append({'id':i.uid,'name':i.name,'checked':False})
        else:
            userall = UandC.objects.filter(cid=id)
            for i in userall:
                nm = Person.objects.get(uid=i.uid).name
                datelist.append({'id':i.uid,'name':nm,'checked':False})
        return HttpResponse(json.dumps({"datelist":datelist}))

