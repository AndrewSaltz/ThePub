# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-22 17:15
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0023_sports_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='pic',
            field=versatileimagefield.fields.VersatileImageField(blank=True, upload_to='teampics/'),
        ),
    ]
