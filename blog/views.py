from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from blog.models import UserInfo
from blog import models
from rest_framework.views import APIView,Response
from blog import serializers
from rest_framework import viewsets
from blog.authentication import MyAuth,Mypermission
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser
from rest_framework.pagination import PageNumberPagination



"""
FBV模式
"""
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('ps')
        models.UserInfo.objects.create(name=name,password=password)
        request.session['is_login'] = name
    return render(request,'register.html')

def login(request):
    name = request.session.get('is_login')
    res = models.UserInfo.objects.filter(name=name).first()
    if res:
        tag = models.Tag.objects.filter(project=res.project).first()
        request.session['is_login'] = ''
        return render(request, 'index.html', {'res': res, 'tag': tag})
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        res = models.UserInfo.objects.all().filter(name=name,password=password).first()
        if res:
            tag = res.project.tag.all()
            return render(request, 'index.html',{'res':res,'tag':tag})
        else:
            return HttpResponse('no')
    return render(request,'login.html')

def test(request):
    ret = models.UserInfo.objects.all().exclude(name='wjx1')    # 与filter相反，相当于不等于
    ret = models.UserInfo.objects.raw('select * from blog_project')  # 在django中执行sql语句的方法之一（前面的Userindo相当于没用了）
    for i in ret:
        print(i)
    ret = models.UserInfo.objects.extra(where=["name='wjx1'"])  # 在django中执行sql语句的方法之一
    ret1 = models.UserInfo.objects.all().values('name')
    ret2 = models.UserInfo.objects.all().values_list('name')

    print(ret1,'\n',ret2)
    return HttpResponse (1)


"""
CBV模式
"""
class Test(View):
    def get(self,request):
        print(request.GET.get('name'))
        return HttpResponse('get')

    def post(self,request):
        print(request.POST.get('name'))
        print(request.body)
        print(request.POST)

        return HttpResponse('post')


"""
下面的类继承了APIView，代表着使用了restframework
APIView重写了request，就是把以前的request.body改成了request.data 开始以为蛋用没有，其实后续的组件都因为它得以实现
"""

class TestRDF(APIView):        # restframework中不再使用View，使用APIView
    def get(self,request):
        print(request.GET)
        print(request.data)
        return Response(12121)   # restframework中不再使用Httpresponse，使用Response

    def post(self,request):
        print(request.POST)
        print(request.data)
        return Response(12121)





"""
在settings里app加上"rest_framework"
浏览器里访问http://127.0.0.1:8001/sertest/可以有新的页面
这样就相当于前端访问的接口直接写好了，直接访问url就可以测试后端

这就是响应器组件
"""



"""
认证组件：
在类下面配置一个认证类，使请求先通过某个认证逻辑判断是否符合，符合的话通过，不符合的话不通过
说简单的话特别简单，只需在正常的继承APIView的类下写authentication_classes = 自己写的认证类就可以了
但是认证逻辑得在自己的认证类里写好
而且一般和自己写的登录逻辑相关，要验证token
这就对自己原来的登录逻辑有了要求

也可以在settings里面进行全局配置，所以请求都通过这个认证类


权限组件：
在类下面配置一个权限类，使判断用户是否符合要求，符合的话通过，不符合的话不通过
只需在正常的继承APIView的类下写permission_classes = 自己写的权限类就可以了
判断权限的逻辑在自己的权限类里面
也可以在settings里面进行全局配置，

频率组件：
。。。。。。


解析器组件：
对于发送过来的数据，可以是json，可以是form，可以说urlencode，可以是其他的,
原生的django的request.post只支持urlencode，接受别的数据类型是request.post是空的
restframework可以自己配置解析器解析他们，封装成request.data
通过parser_classe指定解析器
parser_classes = 解析器类，默认就是下面那三种，还有几种，可以自己加

路由控制组件：
符合restframework接口的路由写起来差不多，太麻烦，路由控制组件把urls.py文件搞整洁点
在urls.py文件里，
用
routers = routers.DefaultRouter()
routers.register('userinfo',views.TestModelViewSet)
url(r'',include(routers.urls)),
代替
url(r'^viewsettest/(?P<pk>\d+)', views.TestModelViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'}),),
url(r'^viewsettest/', views.TestModelViewSet.as_view({'get':'list','post':'create'}),),

分页组件：
实现在url里传参，page=1，即显示第一页内容，一页有多少对象由settings里面的page_size控制
使用方法：
导入PageNumberPagination，实例化一个对象，把querry_set对象传入它的paginate_queryset方法，返回值即为分页后的querryset对象

但这只是最简单的使用方法，除了PageNumberPagination还有另外一个分页类，还可以自己继承这两个类实现功能自定义


"""
class AuthTest(APIView):
    authentication_classes = [MyAuth,]
    permission_classes = [Mypermission]

    parser_classes = [JSONParser,FormParser,MultiPartParser]

    def get(self,request):
        pnp = PageNumberPagination()
        user = models.UserInfo.objects.all()
        userlist = pnp.paginate_queryset(user,request,self)
        print(userlist)
        ret = serializers.UserInfoModelSerializers(userlist,many=True)
        print(ret)
        return Response(ret.data)




"""
序列化组件：
序列化serializer还挺复杂的，和视图组件掺和到一起
"""


"""
serializers:序列化类
实现了类的 序列化 和 反序列化

使用方法：
建一个继承serializers.Serializer的models类（看serializer.py文件里的） 分为Serializer和ModelSerializer
注意里面的字段是serializers.CharField()
在视图view.py里，把models.objects作为参数传入它并实例化
返回的数据为它点data即可，这个东西就是可序列化的
post方法也体现了它的反序列化
"""

"""
下面是符合restframework的接口
"""
class TestSerializers(APIView):

    # 查看所有数据
    def get(self,request):
        user = models.UserInfo.objects.all()
        suser = serializers.UserInfoSerializers(user,many=True)  # user为querryset的话需要加many=True
        project = models.Project.objects.all()
        sproject = serializers.ProjectSerializers(project,many=True)   # 对应Serializers
        sm_user = serializers.UserInfoModelSerializers(user,many=True)  # 对应ModelSerializers
        return Response(sm_user.data)

    # 添加一条数据
    def post(self,request):
        res = serializers.UserInfoModelSerializers(data=request.data) # 此处体现了request.data的价值
        print(res)
        if res.is_valid():  # 返回的数据是否正符合ModelSerializers格式
            res.save()    # 新来的符合格式的数据直接存入数据库
            return Response(res.data)
        else:
            return Response(res.errors)  # res.errors为校验不成功的错误信息

class TestDetailSerializers(APIView):

    # 查看一条数据
    def get(self,request,pk):
        user = models.UserInfo.objects.all().filter(id=pk).first()   # 此处一定要是object对象，
        print(user)
        sm_user = serializers.UserInfoModelSerializers(user)   # user为object对象的话不需要加many=True
        print(sm_user)
        print(sm_user.data)
        return Response(sm_user.data)

    # 删除一条数据
    def delete(self,request,pk):
        print('de;ete')
        models.UserInfo.objects.all().filter(id=pk).delete()
        return Response()

    # 更新一条数据
    def put(self,request,pk):
        user = models.UserInfo.objects.all().filter(id=pk).first()
        res = serializers.UserInfoModelSerializers(user, data=request.data)
        if res.is_valid():
            res.save()
            return Response(res.data)
        else:
            return Response(res.errors)



"""
序列化加视图的终极形式：viewsets.ModelViewSet（视图类） + ModelSerializers（序列化类）
下面三行代码和之前的两个类五个方法实现相同的功能
需要url配置对应方法
某一种方法要改的话需要重写父类方法
"""

class TestModelViewSet(viewsets.ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoModelSerializers










