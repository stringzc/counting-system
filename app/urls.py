from django.urls import path,include
from app import views
urlpatterns = [
            path('weixinlogin', views.weixinlogin, name = "weixinlogin")
            ]
