# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-24 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0033_auto_20170323_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='is_disputed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='teams',
            name='coach',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='teams',
            name='nickname',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]