# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-20 11:15
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0039_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='pic',
            field=versatileimagefield.fields.VersatileImageField(default='', upload_to='player/'),
        ),
    ]
