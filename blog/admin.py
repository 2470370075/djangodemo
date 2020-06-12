from django.contrib import admin

# Register your models here.

from blog.models import UserInfo
from blog.models import Tag
from blog.models import Project

admin.site.register(UserInfo)
admin.site.register(Tag)
admin.site.register(Project)