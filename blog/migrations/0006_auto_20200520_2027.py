# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-05-20 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200520_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Project'),
        ),
    ]
