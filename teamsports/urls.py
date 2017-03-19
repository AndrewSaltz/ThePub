from django.conf.urls import url


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
    #url(r'^selectschool/$', views.SelectSchool.as_view(template_name='selectschool.html'), name='SelectSchool'),
    url(r'^schoolview/(?P<school>[0-9]+)/$', views.SchoolView.as_view(template_name='schoolview.html'), name='SchoolView'),
    #Not using these
    url(r'^home/$', views.HomeView.as_view(template_name='homeview.html'), name='HomeView'),
    #url(r'^selectsport/$', views.SelectSport.as_view(template_name='selectsport.html'), name='SelectSport'),
    # User Links
    url(r'^addnotes/(?P<match>[0-9]+)/$', views.AddNotes.as_view(template_name='addnotes.html'), name='AddNotes'),
    url(r'^reportscore/(?P<match>[0-9]+)/$', views.ScoreReport.as_view(template_name='reportscore.html'), name='ScoreReport'),
    url(r'^coachview/$', views.CoachView.as_view(template_name='coachview.html'), name='CoachView'),
    url(r'^editteam/(?P<team>[0-9]+)/$', views.EditTeam.as_view(template_name='editteam.html'), name='EditTeam'),
    url(r'^createprofile/$', views.CreateProfile.as_view(template_name='createprofile.html'), name='CreateProfile'),
    # USE MODELFORM ?? url(r'^editgame/(?P<match>[0-9]+)$', views.EditGame.as_view(template_name='editview.html'), name='EditGame'),
    # url(r^gamestream/$', views.GameStream.as_view(template_name='gamestream.html'), name='GameStream'),
    url(r'^editprofile/$', views.EditProfile.as_view(template_name='editprofile.html'), name='EditProfile'),
    # url(r^contact/$', views.Contact.as_view(template_name='contact.html'), name='Contact'),
    #adding pictures
    url(r'^addpic/(?P<match>[0-9]+)/$', views.AddPic.as_view(template_name='addpic.html'), name='AddPic'),
    url(r'^picadd/(?P<match>[0-9]+)/$', views.PicTest.as_view(template_name='addpic_test.html'), name='PicAdd'),
    url(r'^mypic/$', views.MyPic.as_view(template_name='mypic.html'), name='MyPic'),
    url(r'^photostream/(?P<type>[ABC])/$', views.PhotoStream.as_view(template_name='photostream.html'), name='PhotoStream'),
    url(r'^(?P<pk>[0-9]+)/delete/$',views.DeletePic.as_view(),name='DeletePic'),
    url(r'^picture/(?P<pic>[0-9]+)/$', views.Pic.as_view(template_name='photo.html'), name='picture'),
    url(r'^reportphoto/(?P<pic>[0-9]+)/$', views.ReportPhoto.as_view(template_name='reportphoto.html'), name='ReportPhoto')
]