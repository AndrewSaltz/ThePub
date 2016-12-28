#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django import forms

# Create your models here.
## class ScheduleAdmin(admin.ModelAdmin)

class Sports(models.Model):
    sport = models.AutoField(primary_key=True)
    sport_name = models.CharField(max_length=225, blank=True, null=True)

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

class SchoolAdmin(admin.ModelAdmin):
    fields = ('school_name')

class Teams(models.Model):
    team = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=225, blank=True, null=True)
    sport_id = models.ForeignKey(Sports, models.DO_NOTHING, blank=True, null=True)
    division = models.CharField(max_length=225, blank=True, null=True)
    school = models.ForeignKey(School, models.DO_NOTHING, blank=True, null=True)
    win = models.IntegerField(blank=True, null=True, default=0)
    loss = models.IntegerField(blank=True, null=True, default=0)
    tie = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'teams'
    def __str__(self):
        return '%s %s'% (self.team_name, self.sport_id)

class TeamsAdmin(admin.ModelAdmin):
    model = Teams
    list_display = ('team_name', 'sport_id', 'division', 'school', 'win', 'loss', 'tie')

class Schedule(models.Model):
    match = models.AutoField(primary_key=True)
    match_date = models.DateField(blank=True, null=True)
    home = models.ForeignKey(Teams, related_name='home_set',  blank=True, null=True)
    away = models.ForeignKey(Teams, related_name='away_set', blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'schedule'
    def __str__(self):
        return '%s at %s , %s' % (self.away, self.home, self.match_date)

class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    list_display = ('match_date', 'home', 'away', 'home_score', 'away_score')




