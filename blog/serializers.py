from blog import models
from rest_framework import serializers

"""
基本的serializer类
"""

class UserInfoSerializers(serializers.Serializer):

    name = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.IntegerField()
    create_time = serializers.DateTimeField()
    project = serializers.CharField(source='project.name')  # ForeignKey字段要这么写

class ProjectSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    tag = serializers.CharField(source='tag.all')   # ManyToManyField字段要这么写


"""
ModelSerializer:Serializer的加强版
很方便
这样实现的类和上面的一样
"""
class UserInfoModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        # fields = ['course', 'level', 'solgen', 'why', 'recommand_course', 'course_detail']

class ProjectModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'




