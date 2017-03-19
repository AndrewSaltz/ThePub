# Create your views here.
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from teamsports.models import School, Teams, Schedule, Sports, Photo, GameNotes, Profile, Info
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render, redirect
from teamsports.forms import Contact, SelectTeam, SelectMatch, SelectSport, SelectSchool, UpdateScore, Notes, AddPicture, SelectUser, ReportPhoto
from django.db.models import Q
from django.views.generic import TemplateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from datetime import datetime
from braces.views import GroupRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

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
        q = self.kwargs.get('team')
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
        q = self.kwargs.get('match')
        context['report'] = GameNotes.objects.filter(game=q)
        context['game'] = Schedule.objects.get(match=q)
        context['gamepic'] = Photo.objects.filter(game=q)
        return context

class SportView(TemplateView):
    template_name = "sportview.html"

    def get_context_data(self, **kwargs):
        context = super(SportView, self).get_context_data(**kwargs)
        q = self.kwargs.get('sport')
        context['sport'] = Teams.objects.filter(sport_id=q).order_by('-win')
        context['sport_name'] = Sports.objects.get(sport=q)
        return context

class SchoolView(generic.TemplateView):
    template_name = "schoolview.html"

    def get_context_data(self, **kwargs):
        context = super(SchoolView, self).get_context_data(**kwargs)
        q = self.kwargs.get('school')
        context['school'] = School.objects.get(school=q)
        context['school_list'] = Teams.objects.filter(school=q)
        return context

class CoachView(LoginRequiredMixin, generic.TemplateView):
    template_name = "coachview.html"
    login_url = 'accounts/login/'
    # group_required = [u"coach", u"reporter"]
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super(CoachView, self).get_context_data(**kwargs)
        my_profile = Profile.objects.get(user=self.request.user)
        now = datetime.now()
        context['my_profile'] = my_profile
        context['upcoming'] = Schedule.objects.filter(match_date__gt=now)
        context['newslist'] = Info.objects.filter(priority=0).order_by('reported_on')
        context['important_news'] = Info.objects.filter(priority=1).order_by('reported_on')
        if my_profile.team != None:
            q = my_profile.team
            context['upcoming_team'] = Schedule.objects.filter(Q(home=q) | Q(away=q)).order_by('match_date').select_related('home', 'away')
        else:
             context['upcoming_team'] = None
        return context

class ScoreReport(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'reportscore.html'
    model = Schedule
    fields = ['home_score', 'away_score']
    login_url = 'accounts/login/'
    group_required = [u"coach", u"reporter"]
    raise_exception = True

    def get_object(self):
        q = self.kwargs.get('match')
        obj=Schedule.objects.get(match=q)
        return obj
        # THIS WORKS THIS WORKS THIS WORKS

    def get_context_data(self, **kwargs):
        context = super(ScoreReport, self).get_context_data(**kwargs)
        q = self.kwargs.get('match')
        context['game'] = Schedule.objects.get(match=q)
        return context

    def get_success_url(self, **kwargs):
        q = self.kwargs.get('match')
        if "submit" in self.request.POST:
            url = reverse('GameView', args={q : 'match'})
        else:
            url = reverse('AddNotes', args={q : 'match'})
        return url

class AddNotes(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'addnotes.html'
    model = GameNotes
    fields = ['notes']
    group_required = [u"coach", u"reporter"]
    login_url = 'accounts/login/'

    def form_valid(self, form):
        self.object = form.save(commit=False)  # Not hit database
        self.object.game = Schedule.objects.get(match=(self.kwargs.get('match')))
        self.object.reported_by = self.request.user  # Update user
        self.object.reported_on = datetime.now()  # Update post_date
        self.object.save()  # And finally save your object to database.
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(AddNotes, self).get_context_data(**kwargs)
        q = self.kwargs.get('match')
        context['game'] = Schedule.objects.get(match=q)
        return context

    def get_object(self):
        q = self.kwargs.get('match')
        obj=GameNotes.objects.get(game=q)
        return obj

    def get_success_url(self):
        q = self.kwargs.get('match')
        url = reverse('GameView', args={q : 'match'})
        return url

class EditTeam(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = 'editteam.html'
    model = Teams
    fields = ['pic']
    success_url = reverse_lazy('CoachView')
    login_url = 'accounts/login/'
    group_required = [u"coach", u"staff"]
    raise_exception = True

    #This will matter more with rosters and pictures

    def get_object(self):
        obj=Teams.objects.get(team=self.kwargs.get('team'))
        return obj

    def get_context_data(self, **kwargs):
        context = super(EditTeam, self).get_context_data(**kwargs)
        context['my_team'] = Teams.objects.get(team=self.kwargs.get('team'))
        return context

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

class AddPic(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'addpic.html'
    model = Photo
    fields = ['photo']
    login_url = 'accounts/login/'
    raise_exception = True
    success_message = "Success!"


    def get_context_data(self, **kwargs):
        context = super(AddPic, self).get_context_data(**kwargs)
        q = self.kwargs.get('match')
        context['match'] = Schedule.objects.get(match=q)
        return context

    def form_valid(self, form):
        q = self.kwargs.get('match')
        self.object = form.save(commit=False)  # Not hit database
        self.object.uploaded_by = self.request.user  # Update user
        self.object.upload_date = datetime.now()  # Update post_date
        self.object.game = Schedule.objects.get(match=q)
        self.object.save()  # And finally save your object to database.
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initial = super(AddPic, self).get_initial()
        q = self.kwargs.get('match')
        initial ['game'] = Schedule.objects.get(match=q)
        return initial

    def get_success_url(self):
        if 'submit' in self.request.POST:
            q = self.kwargs.get('match')
            url = reverse('GameView', args={q : 'match'})
        else:
            q = self.kwargs.get('match')
            url = reverse('AddPic', args={q : 'game'})
        return url

class PicTest(FormView):
    form_class = AddPicture
    template = 'addpic_test.html'
    success_url = reverse_lazy('CoachView')

    def get_initial(self):
        initial = super(PicTest, self).get_initial()
        q = self.kwargs.get('match')
        initial ['game'] = Schedule.objects.get(match=q)
        return initial

    def form_valid(self, form):
        form.save(commit=True)
        return super(PicTest, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PicTest, self).get_context_data(**kwargs)
        q = self.kwargs.get('match')
        context['match'] = Schedule.objects.get(match=q)
        return context

class MyPic(ListView):
    #template_name: 'mypic.html'
    model = Photo
    login_url = 'accounts/login/'
    group_required = [u"coach", u"staff", u"fan", u"reporter"]

    def get_context_data(self, **kwargs):
        context = super(MyPic, self).get_context_data(**kwargs)
        user = self.request.user
        context ['pic'] = Photo.objects.filter(uploaded_by=user)
        return context

class DeletePic(LoginRequiredMixin, DeleteView):
    template_name = 'photo_confirm_delete.html'
    model = Photo
    success_url = reverse_lazy('MyPic')
    login_url = 'accounts/login/'

class Gamestream(generic.TemplateView):
    template = 'gamestream.html'

    def get_context_date(self, **kwargs):
        context = super(Gamestream, self).get_context_data(**kwargs)
        context ['game'] = Schedule.objects.all.order_by('match_date')
        return context

class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'edit_profile.html'
    model = Profile
    success_url = reverse_lazy('CoachView')
    fields = ['pic', 'team', 'sport']
    login_url = 'accounts/login/'


    def get_object(self):
        obj = Profile.objects.get(user=self.request.user)
        return obj

    def get_context_data(self, **kwargs):
        context = super(EditProfile, self).get_context_data(**kwargs)
        my_profile = Profile.objects.get(user=self.request.user)
        context['my_profile'] = my_profile
        return context

class CreateProfile(LoginRequiredMixin, CreateView):
    template_name = 'createprofile.html'
    model = Profile
    success_url = reverse_lazy('CoachView')
    login_url = 'accounts/login/'
    fields = ['pic', 'team', 'sport']

class PhotoStream(ListView):
    model = Photo
    template = 'photostream.html'
    paginate_by = 10

    def get_queryset(self):  #"A" means today, "B" means recent, "C" means by rating when we figure that out
        q = self.kwargs.get('type')
        now = datetime.now()
        if q == "A":
            queryset = Photo.objects.filter(upload_date=now)
        else:
            queryset = Photo.objects.all().order_by('upload_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PhotoStream, self).get_context_data(**kwargs)
        now = datetime.now()
        recent_list = Photo.objects.all().order_by('upload_date')
        select_user_form = SelectUser(self.request.GET or None)
        context['today'] = Photo.objects.filter(upload_date=now)
        context['recent_list'] = recent_list
        context['select_user_form'] = select_user_form
        return context

class Pic(TemplateView):
    template = 'photo.html'

    def get_context_data(self, **kwargs):
        context = super(Pic, self).get_context_data(**kwargs)
        the_photo = Photo.objects.get(id=self.kwargs.get('pic'))
        context['the_photo'] = the_photo
        return context

class ReportPhoto(FormView):
    template = 'reportphoto.html'
    form_class = ReportPhoto
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(ReportPhoto, self).get_context_data(**kwargs)
        the_photo = Photo.objects.get(id=self.kwargs.get('pic'))
        context['the_photo'] = the_photo
        return context

    def form_valid(self, form):
        reporter = Photo.objects.get(id=self.kwargs.get('pic')).uploaded_by,
        user = self.request.user,
        reason = form.cleaned_data['reason'],
        mail = EmailMultiAlternatives(
            subject="Reported Picture by %s" % reporter,
            body="%s reported this photo for %s" % (user, reason),
            from_email="amsaltz@gmail.com",
            to=["amsaltz@philasd.org"],
            )
        mail.send()
        return super(ReportPhoto, self).form_valid(form)

class Contact(FormView):
    template = 'contact.html'
    form_class = Contact
    success_url = reverse_lazy('home')

