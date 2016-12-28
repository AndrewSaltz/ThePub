# Create your views here.
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from teamsports.models import School, Teams, Schedule, Sports
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, redirect
from teamsports.forms import SelectTeam, SelectMatch, SelectSport, SelectSchool, ReportScore
from django.db.models import Q
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    schools = School.objects.all()
    return render(request, 'teamsports/home.html', {'schools' : schools})

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
        context['game'] = Schedule.objects.get(match=q)
        return context

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


class SportView(generic.TemplateView):
    template_name = "sportview.html"

    def get_context_data(self, **kwargs):
        context = super(SportView, self).get_context_data(**kwargs)
        q = self.request.GET.get('sport')
        context['sport'] = Teams.objects.filter(sport_id=q).order_by('win')
        context['sport_name'] = Sports.objects.get(sport=q)
        return context

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

class SchoolView(generic.TemplateView):
    template_name = "schoolview.html"

    def get_context_data(self, **kwargs):
        context = super(SchoolView, self).get_context_data(**kwargs)
        q = self.request.GET.get('school')
        context['school'] = School.objects.get(school=q)
        context['school_list'] = Teams.objects.filter(school=q)
        #Need to add Next Game function...maybe in models?
        return context

class CoachView(LoginRequiredMixin, generic.TemplateView):
    template_name = "coachview.html"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        context = super(CoachView, self).get_context_data(**kwargs)
        team_form = SelectTeam(self.request.GET or None)
        match_form = SelectMatch(self.request.GET or None)
        context = self.get_context_data(**kwargs)
        context['team_form'] = team_form
        context['match_form'] = match_form
        return self.render_to_response(context)


class ScoreReport(UpdateView):
    template_name = 'reportscore.html'
    model = Schedule
    fields = ['home_score', 'away_score']
    success_url = reverse_lazy('CoachView')

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

    #This will matter more with rosters and pictures

    def get_object(self):
        q = self.request.GET.get('team_name')
        obj=Teams.objects.get(team=q)
        return obj


