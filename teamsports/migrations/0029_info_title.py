# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-17 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0028_auto_20170214_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
