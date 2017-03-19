from django.forms import ModelForm
from teamsports.models import Teams, Schedule, Sports, School, Photo, GameNotes, User
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

class SelectUser(ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), initial=0)

    def clean_data(self):
        data=self.cleaned_data['the_user']
        return data

    class Meta:
        model = School
        fields = ['user']

class AddPicture(ModelForm):
    picture = forms.ImageField()

    class Meta:
        model = Photo
        fields = ['photo', 'team_photo', 'game']

class UpdateScore(ModelForm):
    success_url = '/'
    class Meta:
        model = Schedule
        fields = ['home_score', 'away_score']

class Notes(ModelForm):

    class Meta:
        model = GameNotes
        fields = ['notes']

class ReportPhoto(forms.Form):
    SOME_CHOICES = [
        ('a', 'Inappropriate'),
        ('b', 'Not relavent to the game'),
        ('c','Mean-spirited'),
        ('d', 'Racist/Sexist/Homophobic/In violation of The Pub ToS'),
        ('e','Other')
        ]

    reason = forms.MultipleChoiceField(choices=SOME_CHOICES)
    notes = forms.CharField(required=False)
    email = forms.EmailField(required=False)

class Contact(forms.Form):
    REASONS = [
        ('A', 'Question'),
        ('B', 'Bug Report'),
        ('C', 'Other Issue'),
    ]

    reason = forms.ChoiceField(choices=REASONS)
    notes = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(required=False)
