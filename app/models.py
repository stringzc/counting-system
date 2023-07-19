from django.db import models

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
    images =  models.CharField(max_length=100,verbose_name='images')

class Course(models.Model):
    # int id
    cid = models.IntegerField(verbose_name='cid')
    # str classs
    classs = models.CharField(max_length=20,verbose_name='classs')
    # str images
    images = models.CharField(max_length=100,verbose_name='images')
    # str description
    description =  models.CharField(max_length=300,verbose_name='description')

class UandC(models.Model):
    # int id
    uid = models.IntegerField(verbose_name='uid')
    # int id
    cid = models.IntegerField(verbose_name='cid')
    # int times
    times = models.IntegerField(verbose_name='times')



