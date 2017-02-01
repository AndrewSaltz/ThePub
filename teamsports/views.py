# Create your views here.
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from teamsports.models import School, Teams, Schedule, Sports, Photo, GameNotes
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, redirect
from teamsports.forms import SelectTeam, SelectMatch, SelectSport, SelectSchool
from django.db.models import Q
from django.views.generic import TemplateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
from braces.views import GroupRequiredMixin

def home(request):
    now = datetime.now()
    #Not using this, but save for later
    games = Schedule.objects.filter(match_date__gt=now).order_by('match_date')
    last = Schedule.objects.filter(match_date__lte=now).order_by('-match_date')
    # All Sports
    sport_list = Sports.objects.filter(is_current=True)
    return render(request, 'teamsports/home.html', {'games' : games, 'last' : last, 'sport_list' : sport_list })

class StandingsView(FormView):
    form_class = SelectTeam
    template_name = 'teamsports/standings.html'
    model = Teams
    success_url = '/teamview/'

    def form_valid(self, form):
       team = form.cleaned_data['data']
       return render('teamview', {'team' : team})

    def form_invalid(self,form):
        HttpResponse ("This didn't work")


class TeamView(generic.TemplateView):
    template_name = "teamsports/teamview.html"

    def get_context_data(self, **kwargs):
        context = super(TeamView, self).get_context_data(**kwargs)
        q = self.request.GET.get('team_name')
        context['team'] = Teams.objects.get(team=q)
        game_list=Schedule.objects.filter(Q(home=q) | Q(away=q)).order_by('match_date').select_related('home', 'away')
        context['game_list']=game_list
        context['pictures']=Photo.objects.all()
        return context

class MatchSelect(FormView):
    form_class = SelectMatch
    template_name = 'selectmatch.html'
    model = Schedule
    success_url = '/gameview/'

    def form_valid(self,form):
        game = form.clean_data['data']
        return render('gameview', {'game' : game})

    def form_invalid(self,form):
        HttpResponse ("This didn't work")

class GameView(generic.TemplateView):
    template_name = "matchview.html"

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        q = self.request.GET.get('match')
        context['report'] = GameNotes.objects.filter(game=q)
        context['game'] = Schedule.objects.get(match=q)
        context['gamepic'] = Photo.objects.filter(game=q)
        return context
"""
class SelectSport(FormView):
    form_class = SelectSport
    template_name = 'selectsport.html'
    model = Sports
    success_url = '/sportview/'

    def form_valid(self,form):
        sport = form.clean_data['data']
        return render('sportview', {'sport' : sport})

    def form_invalid(self,form):
        HttpResponse ("This didn't work")
"""

class SportView(TemplateView):
    template_name = "sportview.html"

    def get_context_data(self, **kwargs):
        context = super(SportView, self).get_context_data(**kwargs)
        q = self.request.GET.get('sport')
        context['sport'] = Teams.objects.filter(sport_id=q).order_by('-win')
        context['sport_name'] = Sports.objects.get(sport=q)
        return context
"""
class SelectSchool(FormView):
    form_class = SelectSchool
    template_name = 'selectsport.html'
    model = Sports
    success_url = '/schoolview/'

    def form_valid(self, form):
        school = form.clean_data['data']
        return render('schoolview', {'school' : school})

    def form_invalid(self,form):
        HttpResponse ("This didn't work")
"""
class SchoolView(generic.TemplateView):
    template_name = "schoolview.html"

    def get_context_data(self, **kwargs):
        context = super(SchoolView, self).get_context_data(**kwargs)
        q = self.request.GET.get('school')
        context['school'] = School.objects.get(school=q)
        context['school_list'] = Teams.objects.filter(school=q)
        return context

class CoachView(GroupRequiredMixin, generic.TemplateView):
    template_name = "coachview.html"
    login_url = '/login/'
    group_required = [u"coach", u"staff"]
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        context = super(CoachView, self).get_context_data(**kwargs)
        team_form = SelectTeam(self.request.GET or None)
        match_form = SelectMatch(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['team_form'] = team_form
        context['match_form'] = match_form
        return self.render_to_response(context)

class ScoreReport(UpdateView, GroupRequiredMixin):
    template_name = 'reportscore.html'
    model = Schedule
    fields = ['home_score', 'away_score']
    success_url = reverse_lazy('CoachView')
    login_url = '/login/'
    group_required = [u"coach", u"staff", u"reporter"]

    def get_object(self):
        q = self.request.GET.get('match')
        obj=Schedule.objects.get(match=q)
        return obj
        # THIS WORKS THIS WORKS THIS WORKS

class EditTeam(UpdateView):
    template_name = 'editteam.html'
    model = Teams
    fields = ['team_name']
    success_url = reverse_lazy('CoachView')
    login_url = '/login/'
    group_required = [u"coach", u"staff"]

    #This will matter more with rosters and pictures

    def get_object(self):
        q = self.request.GET.get('team_name')
        obj=Teams.objects.get(team=q)
        return obj

class HomeView(generic.TemplateView):
    template_name = "homeview.html"

    def get(self, request, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        select_team_form = SelectTeam(self.request.GET or None)
        select_match_form = SelectMatch(self.request.GET or None)
        select_sport_form = SelectSport(self.request.GET or None)
        select_school_form = SelectSchool(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context ['select_team_form'] = select_team_form
        context ['select_match_form'] = select_match_form
        context ['select_sport_form'] = select_sport_form
        context ['select_school_form'] = select_school_form
        return self.render_to_response(context)

class AddPic(CreateView):
    template_name = 'addpic.html'
    model = Photo
    fields = ['photo', 'game']
    login_url = '/login/'
    group_required = [u"coach", u"staff", u"fan", u"reporter"]

    def form_valid(self, form):
        self.object = form.save(commit=False)  # Not hit database
        self.object.uploaded_by = self.request.user  # Update user
        self.object.upload_date = datetime.now()  # Update post_date
        self.object.save()  # And finally save your object to database.
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initial = super(AddPic, self).get_initial()
        q = self.request.GET.get('game')
        initial ['game'] = Schedule.objects.get(match=q)
        return initial

    def get_success_url(self):
        q = self.request.GET.get('game')
        url = ('/gameview/?match=%s' % q)
        return url

class MyPic(ListView):
    #template_name: 'mypic.html'
    model = Photo
    login_url = '/login/'
    group_required = [u"coach", u"staff", u"fan", u"reporter"]

    def get_context_data(self, **kwargs):
        context = super(MyPic, self).get_context_data(**kwargs)
        user = self.request.user
        context ['pic'] = Photo.objects.filter(uploaded_by=user)
        return context

class DeletePic(DeleteView):
    template_name = 'photo_confirm_delete.html'
    model = Photo
    success_url = reverse_lazy('MyPic')
