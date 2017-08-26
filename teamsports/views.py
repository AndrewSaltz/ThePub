# Create your views here.
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from teamsports.models import School, Teams, Schedule, Sports, Photo, GameNotes, Profile, Info, User, Player
from django.shortcuts import HttpResponseRedirect, render
from teamsports.forms import UpdateTeam, Contact, SelectTeam, SelectMatch, SelectSport, SelectSchool, UpdateScore, AddPicture, ReportPhoto, EditProfile
from django.db.models import Q
from django.views.generic import TemplateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from braces.views import GroupRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from actstream import action
from actstream.models import model_stream
from watson import search as watson
from django.template.loader import render_to_string, get_template


class Home(TemplateView):
    template_name = 'teamsports/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        now = datetime.now()
        context['games'] = Schedule.objects.filter(match_date__gt=now).order_by('match_date')
        context['last'] = Schedule.objects.filter(match_date__lte=now).order_by('-match_date')
        # All Sports
        context['sport_list'] = Sports.objects.filter(is_current=True).order_by('-sport_name')
        # Activity Feed
        stream_one = model_stream(Photo)
        stream_two = model_stream(Schedule)
        stream_three = model_stream(GameNotes)
        context['stream'] = stream_one | stream_two | stream_three
        # Get profile for an authenticated user
        # NO, it's not DRY but the inclusion tag isn't working. Eat butt
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user) or None
            if my_profile:
                q = my_profile.team
                context['game'] = Schedule.objects.filter(Q(home=q) | Q(away=q)).filter(match_date__year=now.year).filter(match_date__month=now.month).filter(match_date__day=now.day)
            else:
                pass
        return context


class StandingsView(FormView):
    # List all teams
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
    # View a specific team
    template_name = "teamsports/teamview.html"

    def get_context_data(self, **kwargs):
        context = super(TeamView, self).get_context_data(**kwargs)
        q = self.kwargs.get('team')
        context['team'] = Teams.objects.get(team=q)
        game_list=Schedule.objects.filter(Q(home=q) | Q(away=q)).order_by('match_date').select_related('home', 'away')
        context['game_list'] = game_list
        context['pictures'] = Photo.objects.all()
        context['roster'] = Player.objects.filter(spring_2017_team=q).filter(is_captain=False)
        context['captain'] = Player.objects.filter(spring_2017_team=q).filter(is_captain=True)
        return context

class MatchSelect(FormView):
    # Choose a specific game
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
    # View a specific game
    template_name = "matchview.html"

    def get_context_data(self, **kwargs):
        context = super(GameView, self).get_context_data(**kwargs)
        q = self.kwargs.get('match')
        context['report'] = GameNotes.objects.filter(game=q)
        context['game'] = Schedule.objects.get(match=q)
        context['gamepic'] = Photo.objects.filter(game=q)
        return context

class SportView(TemplateView):
    # View a sport
    template_name = "sportview.html"

    def get_context_data(self, **kwargs):
        # now().date is the way to go over datetime.now()
        now = datetime.now().date()
        context = super(SportView, self).get_context_data(**kwargs)
        q = self.kwargs.get('sport')
        context['sport'] = Teams.objects.filter(sport_id=q).order_by('-win')
        context['sport_name'] = Sports.objects.get(sport=q)
        context['upcoming'] = Schedule.objects.filter(Q(home__sport=q) | Q(away__sport=q)).filter(match_date__gte=now)
        context['recent'] = Schedule.objects.filter(Q(home__sport=q) | Q(away__sport=q)).filter(match_date__lte=now)
        # Activity Feed, sorting done in template
        context['stream'] = model_stream(Schedule)
        return context


class SchoolView(generic.TemplateView):
    template_name = "schoolview.html"

    def get_context_data(self, **kwargs):
        context = super(SchoolView, self).get_context_data(**kwargs)
        q = self.kwargs.get('school')
        context['school'] = School.objects.get(school=q)
        context['school_list'] = Teams.objects.filter(school=q)
        return context

class CoachView(GroupRequiredMixin, generic.TemplateView):
    template_name = "coachview.html"
    login_url = 'accounts/login/'
    group_required = [u"Coach", u"Reporter"]
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super(CoachView, self).get_context_data(**kwargs)
        user = self.request.user
        # Use my_profile twice, so I declare it here
        my_profile = Profile.objects.get(user=self.request.user)
        now = datetime.now().date()
        context['my_profile'] = my_profile
        context['upcoming'] = Schedule.objects.filter(match_date__gt=now)
        context['newslist'] = Info.objects.filter(priority=0).order_by('reported_on')
        context['important_news'] = Info.objects.filter(priority=1).order_by('reported_on')
        # If the user has a preffered team
        if my_profile.team != None:
            q = my_profile.team
            context['upcoming_team'] = Schedule.objects.filter(Q(home=q) | Q(away=q)).order_by('match_date').select_related('home', 'away')
            # NO, it's not DRY but the inclusion tag isn't working. Eat butt
            context['game'] = Schedule.objects.filter(Q(home=q) | Q(away=q)).filter(match_date=now)
        else:
             context['upcoming_team'] = None

        # I think the Template Tag renders this useless. Also, it won't work with match_date/now date.
        if user.groups == "Coach":
            q = my_profile.team
            games = Schedule.objects.filter(Q(home=q) | Q(away=q)).filter(match_date=now)
            if games:
                context['game_alert'] = True
            else:
                context['game_alert'] = False
        else:
            pass
        return context

class ScoreReport(GroupRequiredMixin, UpdateView):
    template_name = 'reportscore.html'
    model = Schedule
    form_class = UpdateScore
    login_url = '/accounts/login/'
    group_required = [u"Coach", u"Reporter"]
    raise_exception = False

    def get_object(self):
        # Grab the right game
        q = self.kwargs.get('match')
        obj=Schedule.objects.get(match=q)
        return obj

    def get_context_data(self, **kwargs):
        context = super(ScoreReport, self).get_context_data(**kwargs)
        q = self.kwargs.get('match')
        context['game'] = Schedule.objects.get(match=q)
        return context

    def form_valid(self, form):
        action.send(self.request.user, verb='reported a score', target=self.object) # Activity Stream
        return super(ScoreReport, self).form_valid(form)

    def get_success_url(self, **kwargs):
        q = self.kwargs.get('match')
        if "submit" in self.request.POST:
            url = reverse('GameView', args={q : 'match'})
        # Submit and add a note
        elif "notes" in self.request.POST:
            url = reverse('AddNotes', args={q : 'match'})
        return url

class AddNotes(GroupRequiredMixin, CreateView):
    template_name = 'addnotes.html'
    model = GameNotes
    fields = ['notes']
    group_required = [u"Coach", u"Reporter"]
    login_url = "accounts/login/"
    raise_exception = False

    def form_valid(self, form):
        self.object = form.save(commit=False)  # Not hit database
        self.object.game = Schedule.objects.get(match=(self.kwargs.get('match')))
        self.object.reported_by = self.request.user  # Update user
        self.object.reported_on = datetime.now()  # Update post_date
        self.object.save()  # And finally save your object to database.
        action.send(self.request.user, verb='added a note', target=self.object, action_object=self.object) # Activity Stream
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
    login_url = 'accounts/login/'
    group_required = [u"Coach", u"Staff"]
    raise_exception = False
    form_class = UpdateTeam

    def get_object(self):
        obj=Teams.objects.get(team=self.kwargs.get('team'))
        return obj

    def get_context_data(self, **kwargs):
        context = super(EditTeam, self).get_context_data(**kwargs)
        context['my_team'] = Teams.objects.get(team=self.kwargs.get('team'))
        return context

    def get_success_url(self):
        q = self.kwargs.get('team')
        url = reverse('TeamView', kwargs={'team':q})
        return url

from django.forms import BaseModelFormSet
from teamsports.forms import  UpdatePlayerFormset, DeletePlayerFormset, AddPlayerFormset
from django.forms.models import modelformset_factory



class EditRoster(GroupRequiredMixin, FormView):
    template_name = "editroster.html"
    login_url = 'accounts/login/'
    group_required = [u"Coach", u"Staff"]
    raise_exception = False
    model = Player
    form_class = AddPlayerFormset

    def get_success_url(self):
        q = self.kwargs.get('team')
        url = reverse('TeamView', args={q : 'match'})
        return url


    def get_context_data(self, **kwargs):
        context = super(EditRoster, self).get_context_data(**kwargs)
        q = self.kwargs.get('team')
        context['team'] = Teams.objects.get(team=q)
        return context

'''
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
'''

class AddPic(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'addpic.html'
    model = Photo
    fields = ['photo']
    login_url = 'accounts/login/'
    raise_exception = False
    success_message = "Success!"


    def get_context_data(self, **kwargs):
        context = super(AddPic, self).get_context_data(**kwargs)
        q = self.kwargs.get('match')
        context['match'] = Schedule.objects.get(match=q)
        return context

    def form_valid(self, form):
        out = super(AddPic, self).form_valid(form)
        q = self.kwargs.get('match')
        self.object = form.save(commit=False)  # Not hit database
        self.object.uploaded_by = self.request.user  # Update user
        self.object.upload_date = datetime.now()  # Update post_date
        self.object.game = Schedule.objects.get(match=q)
        self.object.save()  # And finally save your object to database.
        action.send(self.request.user, verb='posted a picture', target=self.object, action_object=self.object) # Activity Stream
        return out

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
        # Submit and add another
            q = self.kwargs.get('match')
            url = reverse('AddPic', args={q : 'game'})
        return url

'''
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
'''

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


class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'edit_profile.html'
    model = Profile
    success_url = reverse_lazy('CoachView')
    login_url = 'accounts/login/'
    form_class = EditProfile

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

class PhotoStream(FormMixin,ListView):
    model = Photo
    template = 'photostream.html'
    paginate_by = 10
    form_class = SelectTeam

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
        now = timezone.now().date()
        recent_list = Photo.objects.all().order_by('-upload_date')
        context['today'] = Photo.objects.filter(upload_date__startswith=now)
        context['recent_list'] = recent_list
        context['username'] = self.request.user.pk
        return context

    def form_valid(self, form):
        team = form.clean_data['data']
        return reverse_lazy('TeamPhotoStream', {'team' : team})

class TeamPhotoStream(FormMixin, ListView):
    model = Photo
    template = 'photostream.html'
    paginate_by = 10
    form_class = SelectTeam

    def get_queryset(self):
        q = self.kwargs.get('team')
        queryset = Photo.objects.filter(Q(game__home=q) | Q(game__away=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TeamPhotoStream, self).get_context_data(**kwargs)
        q = self.request.GET.get('team_name')
        if q == None:
            context['team'] = 0
            context['team_photo'] = 0
        else:
            context['team'] = Teams.objects.get(team=q)
            context['team_photo'] = Photo.objects.filter(Q(game__home=q) | Q(game__away=q))
        return context

    def form_valid(self, form):
        team = form.clean_data['data']
        return reverse_lazy('TeamPhotoStream', {'team' : team})

class MyPhotoStream(LoginRequiredMixin, FormMixin, ListView):
    template = 'myphotostream.html'
    model = Photo
    form_class = SelectTeam


    def get_queryset(self):
        q = self.kwargs.get('user')
        user = User.objects.get(pk=q)
        queryset = Photo.objects.filter(uploaded_by=user)
        return queryset

    def form_valid(self, form):
        team = form.clean_data['data']
        return reverse_lazy('TeamPhotoStream', {'team' : team})

class Pic(TemplateView):
    template = 'photo.html'

    def get_context_data(self, **kwargs):
        context = super(Pic, self).get_context_data(**kwargs)
        the_photo = Photo.objects.get(id=self.kwargs.get('pic'))
        context['the_photo'] = the_photo
        return context

from django.core.mail import EmailMessage

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
        now = datetime.now()
        the_photo = Photo.objects.get(id=self.kwargs.get('pic'))
        reason = form.cleaned_data['reason']
        msg_html = render_to_string('error_template.html', {'the_photo': the_photo, 'user': self.request.user, 'notes': self.request.POST.get('notes'), 'reason': reason, 'email' : self.request.POST.get('email')})
        send_mail(
            subject='Picture Alert!',
            message='Picture Report!',
            from_email ='amsaltz@gmail.com',
            recipient_list = ['amsaltz@philasd.org'],
            html_message=msg_html,
            )
        return super(ReportPhoto, self).form_valid(form)

from django.template import Context

class Contact(FormView):
    template = 'contact.html'
    form_class = Contact
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        now = datetime.now()
        contact_name = self.request.POST.get('contact_name', '')
        contact_email = self.request.POST.get('contact_email', '')
        form_content = self.request.POST.get('content', '')

            # Email the profile with the
            # contact information
        template = get_template('contact.txt')
        context = Context({
            'contact_name': contact_name,
            'contact_email': contact_email,
            'form_content': form_content,
            })
        content = template.render(context)
        send_mail(
            subject="New contact form submission",
            message=content,
            from_email = contact_email,
            recipient_list = ['amsaltz@philasd.org'],
            )
        return super(Contact, self).form_valid(form)


class Searcher(generic.TemplateView):
    template = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(Searcher, self).get_context_data(**kwargs)
        term = self.request.GET.get('search')
        context['results'] = watson.search(term)
        return context

class GameStream(ListView, FormMixin):
    model = Schedule
    template = "gamestream.html"
    form_class = SelectTeam

    def get_queryset(self):
        q = self.kwargs.get('type')
        today = datetime.now().date()
        if q=="today":
            queryset = Schedule.objects.filter(match_date=today)
        elif q=="recent":
            three_days = (today - timedelta(days=3))
            queryset = Schedule.objects.filter(match_date__gte=three_days).filter(match_date__lte=today)
        elif q == "upcoming":
            future = (today + timedelta(days=3))
            queryset = Schedule.objects.filter(match_date__lte=future).filter(match_date__gte=today)
        else:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GameStream, self).get_context_data(**kwargs)
        q = self.kwargs.get('type')
        today = datetime.now().date()
        if q=="today":
            context['object_list'] = Schedule.objects.filter(match_date=today)
        elif q=="recent":
            three_days = (today - timedelta(days=3))
            context['object_list'] = Schedule.objects.filter(match_date__gte=three_days).filter(match_date__lte=today)
        elif q == "upcoming":
            future = (today + timedelta(days=3))
            context['object_list'] = Schedule.objects.filter(match_date__lte=future).filter(match_date__gte=today)
        return context

    def form_valid(self, form):
        team = form.clean_data['data']
        return reverse_lazy('TeamGameStream', {'team' : team})

class TeamGameStream(ListView, FormMixin):
    model = Schedule
    form_class = SelectTeam
    template = 'gamestream.html'

    def get_queryset(self):
        q = self.request.GET.get('team_name')
        queryset = Schedule.objects.filter(Q(home=q) | Q(away=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TeamGameStream, self).get_context_data(**kwargs)
        q = self.request.GET.get('team_name')
        if q == None:
            context['team'] = 0
        else:
            context['team'] = Teams.objects.get(team=q)
        return context

class About(TemplateView):
    template = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        context['newslist'] = Info.objects.filter(priority=0).order_by('reported_on')
        context['important_news'] = Info.objects.filter(priority=1).order_by('reported_on')
        return context
