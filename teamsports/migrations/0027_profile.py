# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-03 19:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teamsports', '0026_auto_20170122_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', versatileimagefield.fields.VersatileImageField(blank=True, default='', upload_to='profile/')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamsports.Teams')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
