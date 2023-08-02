from django.urls import path,include
from app import views
urlpatterns = [
            path('',views.index,name="index"),
            path('weixinlogin', views.weixinlogin, name = "weixinlogin"),
            path('getclass',views.getclass, name = "getclass"),
            path('myclass',views.myclass, name = 'myclass')
            ]
