from django.urls import path,include
from app import views
urlpatterns = [
            path('',views.index,name="index"),
            path('weixinlogin', views.weixinlogin, name = "weixinlogin"),
            path('getclass',views.getclass, name = "getclass"),
            path('myclass',views.myclass, name = 'myclass'),
            path('findQD',views.findQD,name='findQD'),
            path('QD',views.QD,name='QD'),
            path('bdfind',views.bdfind,name='bdfind'),
            path('tuike',views.tuike,name='tuike'),
            path('bd',views.bd,name='bd'),
            path('weixinregistered',views.weixinregistered,name='weixinregistered'),
            path('logs',views.logs,name='logs'),
            path('pluns',views.pluns,name='pluns'),
            path('gethots',views.gethots,name='gethots'),
            path('getallcls',views.getallcls,name='getallcls'),
            path('getuserdate',views.getuserdate,name='getuserdate')
            ]
