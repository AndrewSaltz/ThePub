from django.forms import ModelForm
from teamsports.models import Teams, Schedule, Sports, School, Photo, GameNotes, User, Profile, Player
from django import forms
from django.forms import widgets, HiddenInput
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, redirect

class SelectTeam(ModelForm):
    #team = forms.ModelChoiceField(queryset=Teams.objects.all(), widget=forms.HiddenInput())
    team_name = forms.ModelChoiceField(queryset=Teams.objects.filter(sport__is_current=True), initial=0)

    def clean_data(self):
        data=self.cleaned_data['team']
        return data

    class Meta:
        model = Teams
        fields = ['team']

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
        fields = ['home_score', 'away_score', 'is_disputed']
        is_disputed = forms.BooleanField(initial=False, required=False)

class Notes(ModelForm):

    class Meta:
        model = GameNotes
        fields = ['notes']

class ReportPhoto(forms.Form):
    SOME_CHOICES = [
        ('inappropirate', 'Inappropriate'),
        ('not relavent', 'Not relavent to the game'),
        ('mean-spirited','Mean-spirited'),
        ('racist', 'Racist/Sexist/Homophobic/In violation of The Pub ToS'),
        ('other','Other')
        ]

    reason = forms.MultipleChoiceField(choices=SOME_CHOICES)
    notes = forms.CharField(required=False)
    email = forms.EmailField(required=False)

class Contact(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    # the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"

class EditProfile(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditProfile, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['pic'].required = False
        self.fields['team'].required = False


    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'pic', 'team']

class UpdateTeam(ModelForm):


    class Meta:
        model = Teams
        fields = ['coach', 'nickname', 'division', 'pic']

from django.forms import BaseModelFormSet
from django.forms import modelformset_factory

class AddPlayer(forms.ModelForm):

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'pic', 'spring_2017_team']

class CreatePlayerFormset(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        q = kwargs.get('team')
        super(CreatePlayerFormset, self).__init__(*args, **kwargs)
        self.queryset = Player.objects.filter(spring_2017_team = q)


AddPlayerFormset = modelformset_factory(Player, fields=('first_name', 'last_name', 'pic', 'is_captain', 'spring_2017_team'), extra=10, formset = CreatePlayerFormset)

class DeletePlayer(ModelForm):

    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'pic']


class UpdatePlayer(ModelForm):

   class Meta:
       model = Player
       fields = ['first_name', 'last_name', 'pic']

from django.forms.models import modelformset_factory
from django.forms import BaseModelFormSet

DeletePlayerFormset = modelformset_factory(Player, form = DeletePlayer, fields = ('first_name', 'last_name', 'is_captain', 'pic'))
UpdatePlayerFormset = modelformset_factory(Player, form = UpdatePlayer, fields = ('first_name', 'last_name','is_captain', 'pic'))