# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-14 01:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0004_auto_20161114_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='played',
        ),
    ]
