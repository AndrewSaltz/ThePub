#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from versatileimagefield.fields import VersatileImageField
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
## class ScheduleAdmin(admin.ModelAdmin)

class Sports(models.Model):
    sport = models.AutoField(primary_key=True)
    sport_name = models.CharField(max_length=225, blank=True, null=True)
    is_current = models.BooleanField(default=False)
    pic = VersatileImageField(upload_to='sportpics/', blank=True)

    class Meta:
        managed = True
        db_table = 'sports'
    def __str__(self):
        return self.sport_name

class SportAdmin(admin.ModelAdmin):
    list_display = ('sport_name', 'is_current', 'pic')

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
    coach = models.CharField(max_length=225, blank=True, null=True)
    nickname = models.CharField(max_length=225, blank=True, null=True)
    win = models.IntegerField(blank=True, null=True, default=0)
    loss = models.IntegerField(blank=True, null=True, default=0)
    tie = models.IntegerField(blank=True, null=True, default=0)
    pic = VersatileImageField(upload_to='teampics/', blank=True, default='/teampics/emptyfield.jpg')

    def next_game(self):
        dt=datetime.now()
        h = Schedule(home=self.team).filter(match_date__gt=dt).order_by("match_date")
        a = Schedule(away=self.team).filter(match_date__gt=dt).order_by("match_date")
        return 'Next home game %s, Next away game %s' % (h, a)

    class Meta:
        db_table = 'teams'
    def __str__(self):
        return '%s %s' % (self.school, self.sport)
# changed, see  team_name

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('team', 'sport', 'division', 'school', 'win', 'loss', 'tie', 'pic')

from jsonfield import JSONField

class Schedule(models.Model):
    match = models.AutoField(primary_key=True)
    match_date = models.DateField(blank=True, null=True)
    home = models.ForeignKey(Teams, related_name='home_set',  blank=True, null=True)
    away = models.ForeignKey(Teams, related_name='away_set', blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True, default=None)
    away_score = models.IntegerField(blank=True, null=True, default=None)
    is_disputed = models.BooleanField(default=False, blank=True)
    json = JSONField()

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
    upload_date = models.DateTimeField(default=datetime.now)
    photo = VersatileImageField(upload_to='gamepics/', blank=False)
    uploaded_by = models.ForeignKey('auth.User', null=True)

class GameNotes(models.Model):
    game = models.ForeignKey(Schedule, blank=True, null=True)
    notes = models.TextField(blank=True, null=True, default=None)
    reported_by = models.ForeignKey('auth.User', blank=True, null=True)
    reported_on = models.DateTimeField(auto_now_add=True, null=True)

class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, null=False)
    pic = VersatileImageField(upload_to='profile/', blank=True, null=True)
    team = models.ForeignKey(Teams, blank=True, null=True)
    sport = models.ForeignKey(Sports, blank=True, null=True)
    first_name = models.CharField(max_length=225,blank=True, null=True)
    last_name = models.CharField(max_length=225,blank=True, null=True)

class Info(models.Model): #For system-wide news
    news = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, blank=False, null=False)
    title = models.TextField(blank=True, null=True)
    reported_on = models.DateTimeField(auto_now_add=True, null=True)
    priority = models.BooleanField(default=False)

#Rosters
from versatileimagefield.placeholder import OnStoragePlaceholderImage
class Player(models.Model):
    first_name = models.CharField(max_length=225, blank=True, null=True)
    last_name = models.CharField(max_length=225, blank=True, null=True)
    spring_2017_team = models.ForeignKey(Teams, blank=False, null=False)
    school = models.ForeignKey(School, blank=False, null=False)
    pic = VersatileImageField(upload_to='player/', null=True, placeholder_image=OnStoragePlaceholderImage('player/blank-person.jpg'))
    is_captain = models.BooleanField(default=False)

# Don't remember if I'm using this
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def do_stuff_after_sign_up(sender, **kwargs):
    user = kwargs['user']
    profile = Profile(user=user)
    profile.save()
    user.save()