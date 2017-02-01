# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-14 13:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamsports', '0017_auto_20170113_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_notes', models.TextField(blank=True, default=None, null=True)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teamsports.Teams')),
            ],
        ),
        migrations.AddField(
            model_name='sports',
            name='is_current',
            field=models.BooleanField(default=False),
        ),
    ]