# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-05-19 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='name2',
            field=models.CharField(default='wjx', max_length=11),
        ),
    ]
