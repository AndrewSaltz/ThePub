from django.conf.urls import url
from django.conf.urls import include, url


from . import views

urlpatterns = [
    # selecting a team - need to change "standings"
    url(r'^standings/$', views.StandingsView.as_view(template_name='teamsports/standings.html'), name='StandingsView'),
    url(r'^teamview/(?P<team>[0-9]+)/$', views.TeamView.as_view(template_name='teamview.html'), name='TeamView'),
    # selecting a game
    url(r'^matchselect/$', views.MatchSelect.as_view(template_name ='selectmatch.html'), name='MatchSelect'),
    url(r'^gameview/(?P<match>[0-9]+)/$', views.GameView.as_view(template_name='matchview.html'), name='GameView'),
    url(r'^sportview/(?P<sport>[0-9]+)/$', views.SportView.as_view(template_name='sportview.html'), name='SportView'),
    # selecting a school
    url(r'^schoolview/(?P<school>[0-9]+)/$', views.SchoolView.as_view(template_name='schoolview.html'), name='SchoolView'),
    # User Links
    url(r'^addnotes/(?P<match>[0-9]+)/$', views.AddNotes.as_view(template_name='addnotes.html'), name='AddNotes'),
    url(r'^reportscore/(?P<match>[0-9]+)/$', views.ScoreReport.as_view(template_name='reportscore.html'), name='ScoreReport'),
    url(r'^coachview/$', views.CoachView.as_view(template_name='coachview.html'), name='CoachView'),
    url(r'^editteam/(?P<team>[0-9]+)/$', views.EditTeam.as_view(template_name='editteam.html'), name='EditTeam'),
    url(r'^editroster/(?P<team>[0-9]+)/$', views.EditRoster.as_view(template_name='editroster.html'), name='EditRoster'),
    url(r'^createprofile/$', views.CreateProfile.as_view(template_name='createprofile.html'), name='CreateProfile'),
    url(r'^gamestream/(?P<type>today|recent|upcoming|)/$', views.GameStream.as_view(template_name='gamestream.html'), name='GameStream'),
    # GameStream by Team
    url(r'^teamstream/$',views.TeamGameStream.as_view(template_name='gamestream.html'), name='TeamGameStream'),
    url(r'^editprofile/$', views.EditProfile.as_view(template_name='editprofile.html'), name='EditProfile'),
    url(r'^contact/$', views.Contact.as_view(template_name='contact.html'), name='Contact'),
    # adding pictures
    url(r'^addpic/(?P<match>[0-9]+)/$', views.AddPic.as_view(template_name='addpic.html'), name='AddPic'),
    url(r'^mypic/$', views.MyPic.as_view(template_name='mypic.html'), name='MyPic'),
    url(r'^photostream/(?P<type>[ABC])/$', views.PhotoStream.as_view(template_name='photostream.html'), name='PhotoStream'),
    url(r'^photostream/team/$', views.TeamPhotoStream.as_view(template_name='photostream.html'), name='TeamPhotoStream'),
    url(r'^(?P<pk>[0-9]+)/delete/$',views.DeletePic.as_view(),name='DeletePic'),
    url(r'^picture/(?P<pic>[0-9]+)/$', views.Pic.as_view(template_name='photo.html'), name='picture'),
    url(r'^reportphoto/(?P<pic>[0-9]+)/$', views.ReportPhoto.as_view(template_name='reportphoto.html'), name='ReportPhoto'),
    url(r'^myphotostream/(?P<user>[0-9]+)/$', views.MyPhotoStream.as_view(template_name='myphotostream.html'), name='MyPhotoStream'),
    # Searching
    url(r'^search/$', views.Searcher.as_view(template_name='search.html'), name='Search'),
    #Misc
    url(r'^about/$', views.About.as_view(template_name='about.html'), name='About')
]