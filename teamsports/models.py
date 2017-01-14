#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from versatileimagefield.fields import VersatileImageField

# Create your models here.
## class ScheduleAdmin(admin.ModelAdmin)

class Sports(models.Model):
    sport = models.AutoField(primary_key=True)
    sport_name = models.CharField(max_length=225, blank=True, null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'sports'
    def __str__(self):
        return self.sport_name


class School(models.Model):
    school = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = True
        db_table= 'school'
    def __str__(self):
        return self.school_name

class Teams(models.Model):
    team = models.AutoField(primary_key=True)
    sport = models.ForeignKey(Sports, models.DO_NOTHING, blank=True, null=True)
    division = models.CharField(max_length=225, blank=True, null=True)
    school = models.ForeignKey(School, models.DO_NOTHING, blank=True, null=True)
    win = models.IntegerField(blank=True, null=True, default=0)
    loss = models.IntegerField(blank=True, null=True, default=0)
    tie = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'teams'
    def __str__(self):
        return '%s %s' % (self.school, self.sport)
# changed, see  team_name


class Schedule(models.Model):
    match = models.AutoField(primary_key=True)
    match_date = models.DateField(blank=True, null=True)
    home = models.ForeignKey(Teams, related_name='home_set',  blank=True, null=True)
    away = models.ForeignKey(Teams, related_name='away_set', blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True, default=None)
    away_score = models.IntegerField(blank=True, null=True, default=None)
    class Meta:
        managed = True
        db_table = 'schedule'
    def __str__(self):
        return '%s at %s , %s' % (self.away, self.home, self.match_date)

class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    list_display = ('match_date', 'home', 'away', 'home_score', 'away_score')

class Photo(models.Model):
    team_photo = models.ForeignKey(Teams, blank=True, null=True)
    game = models.ForeignKey(Schedule, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    photo = VersatileImageField(upload_to='gamepics/', blank=True)
    uploaded_by = models.ForeignKey('auth.User', null=True)

class GameNotes(models.Model):
    game = models.ForeignKey(Schedule, blank=True, null=True)
    notes = models.TextField(blank=True, null=True, default=None)
    reported_by = models.ForeignKey('auth.User', blank=True, null=True)
    reported_on = models.DateTimeField(auto_now_add=True, null=True)




