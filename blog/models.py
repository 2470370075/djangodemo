from django.db import models

class UserInfo(models.Model):

    name = models.CharField(max_length=11,default='wjx')
    password = models.CharField(max_length=11,default='12345')
    token = models.CharField(max_length=100,default='')
    phone = models.CharField(max_length=11, null=True, unique=True,blank=True)
    create_time = models.DateTimeField(null=True,auto_now_add=True)
    project = models.ForeignKey(to='Project',null=True,)

    def __str__(self):
        return self.name

class Project(models.Model):

    name = models.CharField(max_length=20)
    tag = models.ManyToManyField(to='Tag',null=True)
    def __str__(self):
        return self.name

class Tag(models.Model):

    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


