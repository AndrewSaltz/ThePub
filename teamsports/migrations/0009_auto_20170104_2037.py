# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-04 20:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0008_auto_20161120_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teams',
            old_name='sport_id',
            new_name='sport',
        ),
        migrations.RemoveField(
            model_name='teams',
            name='team_name',
        ),
    ]
