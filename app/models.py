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


