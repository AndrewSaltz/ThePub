# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-13 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0016_auto_20170109_1804'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='away_notes',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='home_notes',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='away_score',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='home_score',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]