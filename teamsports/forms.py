from django.forms import ModelForm
from teamsports.models import Teams, Schedule, Sports, School
from django import forms
from django.forms import widgets, HiddenInput
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, redirect



class SelectTeam(ModelForm):
    team = forms.ModelChoiceField(queryset=Teams.objects.all(), widget=forms.HiddenInput())
    team_name = forms.ModelChoiceField(queryset=Teams.objects.all(), initial=0)

    def clean_data(self):
        data=self.cleaned_data['team_name']
        return data

    class Meta:
        model = Teams
        fields = ['team', 'team_name']

class SelectMatch(ModelForm):
    match = forms.ModelChoiceField(queryset=Schedule.objects.all().order_by('match_date'), initial=0)

    class Meta:
        model = Schedule
        fields = ['match']

class SelectSport(ModelForm):
    sport = forms.ModelChoiceField(queryset=Sports.objects.all(), initial=0)

    def clean_data(self):
        data=self.cleaned_data['sport']
        return data

    class Meta:
        model = Sports
        fields = ['sport']

class SelectSchool(ModelForm):
    school = forms.ModelChoiceField(queryset=School.objects.all(), initial=0)

    def clean_data(self):
        data=self.cleaned_data['school']
        return data

    class Meta:
        model = School
        fields = ['school']


#Note sure we need this with Updateview
class ReportScore(ModelForm):
    class Meta:
        model = Schedule
        fields = ['match_date', 'home_score', 'away_score']

