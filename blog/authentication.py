from rest_framework.exceptions import AuthenticationFailed
from blog import models
from rest_framework.authentication import BaseAuthentication

"""
authenticate方法里写具体的认证逻辑

下面只是模拟了一个最简单的认证组件
只要get请求带一个token=1的数据就可以认证通过
"""
class MyAuth(BaseAuthentication):

    def authenticate(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if token == '1':
            user = models.UserInfo.objects.first()
            return (user.name,user)
        else:
            raise AuthenticationFailed({'code':'400'})


"""
has_permission方法里写具体的权限逻辑

下面只是模拟了一个最简单的权限组件
模拟一个per
per为True说明有权限
为False说明没有权限
"""

class Mypermission():
    message='error'                                     #返回的错误信息
    def has_permission(self,request,view):            #必须叫has_permission
        print('permission')
        per=True
        if per:
            return True
        else:
            return False

