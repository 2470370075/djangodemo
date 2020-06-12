from django.conf.urls import url
from django.contrib import admin
from blog import views
from rest_framework import routers
from django.conf.urls import url, include

routers = routers.DefaultRouter()
routers.register('userinfo',views.TestModelViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/',views.register,),
    url(r'^login/', views.login, ),
    url(r'^test/', views.test, ),
    url(r'^cbvtest/', views.Test.as_view(), ),
    url(r'^rdftest/', views.TestRDF.as_view(), ),

    # 加括号可以实现url传参，视图函数里request后面的参数对应括号里的参数
    # 括号前面加上名字叫分组命名，名字要和视图函数里的参数名字一样
    url(r'^sertest/(?P<pk>\d+)', views.TestDetailSerializers.as_view(), ),
    url(r'^sertest/', views.TestSerializers.as_view(), ),

    url(r'',include(routers.urls)),
    # url(r'^viewsettest/(?P<pk>\d+)', views.TestModelViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}),name='userinfo' ),
    # url(r'^viewsettest/', views.TestModelViewSet.as_view({'get':'list','post':'create'}),name='userinfo'  ),

    url(r'^authtest/', views.AuthTest.as_view()),

]
