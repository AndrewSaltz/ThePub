# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-20 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0040_player_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_captain',
            field=models.BooleanField(default=False),
        ),
    ]
