# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-14 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0018_auto_20170114_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamenotes',
            name='away_notes',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='gamenotes',
            name='other_notes',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]