# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-13 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0036_auto_20170513_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
