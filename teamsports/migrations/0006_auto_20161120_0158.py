# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 01:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0005_remove_schedule_played'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='match',
        ),
        migrations.DeleteModel(
            name='Score',
        ),
    ]
