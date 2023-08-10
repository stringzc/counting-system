from django.urls import path,include
from app import views
urlpatterns = [
            path('',views.index,name="index"),
            path('weixinlogin', views.weixinlogin, name = "weixinlogin"),
            path('getclass',views.getclass, name = "getclass"),
            path('myclass',views.myclass, name = 'myclass'),
            path('findQD',views.findQD,name='findQD'),
            path('QD',views.QD,name='QD'),
            path('bdfind',views.bdfind,name='bdfind')
            ]
