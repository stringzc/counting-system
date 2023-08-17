from django.db import models
from django.utils import timezone
# Create your models here.
class Person(models.Model):
    # int id
    uid = models.IntegerField(verbose_name='uid')
    # str name
    name = models.CharField(max_length=20,verbose_name='name')
    # int phone
    phone = models.IntegerField(verbose_name='phone')
    # str password
    password = models.CharField(max_length=20,verbose_name='password')
    # str images
    img = models.ImageField(upload_to='static/img',verbose_name='imgurl')

class Course(models.Model):
    # int id
    cid = models.IntegerField(verbose_name='cid')
    # str classs
    classs = models.CharField(max_length=20,verbose_name='classs')
    # str images
    img = models.ImageField(upload_to='static/img',verbose_name='imgurl')
    # str description
    description =  models.CharField(max_length=300,verbose_name='description')
    descriptionall =  models.CharField(max_length=600,verbose_name='descriptionall')


class UandC(models.Model):
    # int id
    uid = models.IntegerField(verbose_name='uid')
    # int id
    cid = models.IntegerField(verbose_name='cid')
    # int times
    RC = models.IntegerField(verbose_name='RC')
    times = models.DateTimeField(verbose_name='time',null=True)

class UandP(models.Model):
    cid = models.IntegerField(verbose_name='cid')
    power = models.IntegerField(verbose_name='power')

class CandImg(models.Model):
    cid = models.IntegerField(verbose_name='cid')
    keshi = models.IntegerField(verbose_name='keshi')
    show1 = models.ImageField(upload_to='static/img',verbose_name='show1')
    show2 = models.ImageField(upload_to='static/img',verbose_name='show2')
    show3 = models.ImageField(upload_to='static/img',verbose_name='show3')
    show4 = models.ImageField(upload_to='static/img',verbose_name='show4')

class QDI(models.Model):
    qid = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='uid')
    cid = models.IntegerField(verbose_name='cid')
    times = models.DateTimeField(verbose_name='times',null=True)
class DLI(models.Model):
    did = models.AutoField(primary_key=True) 
    IP = models.CharField(max_length=300,verbose_name='IP')
    uid = models.IntegerField(verbose_name='uid')
    times = models.DateTimeField(verbose_name='times',null=True)

class BDI(models.Model):
    bid = models.AutoField(primary_key=True)
    cid = models.IntegerField(verbose_name='cid')
    times = models.DateTimeField(verbose_name='times',null=True)
    uid = models.IntegerField(verbose_name='uid')

class UCI(models.Model):
    ucid = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='uid')
    times = models.DateTimeField(verbose_name='times',null=True)

class plun(models.Model):
    plid = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='uid')
    title = models.CharField(max_length=100,verbose_name='title') 
    content = models.TextField(verbose_name='content',max_length=1024)
    times = models.DateTimeField(verbose_name='times',null=True)

class black(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name='uid')

class BASIC(models.Model):
    STARTTIME = models.DateTimeField(verbose_name='STARTTIME',null=True)
    Checkincooldown = models.IntegerField(verbose_name='Checkincooldown')
    Commentonthecooldown = models.IntegerField(verbose_name='Commentonthecooldown')
