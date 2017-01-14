from django.conf.urls import url


from . import views

urlpatterns = [
    # selecting a team - need to change "standings"
    url(r'^standings/$', views.StandingsView.as_view(template_name='teamsports/standings.html'), name='StandingsView'),
    url(r'^teamview/$', views.TeamView.as_view(template_name='teamview.html'), name='TeamView'),
    # selecting a game
    url(r'^matchselect/$', views.MatchSelect.as_view(template_name ='selectmatch.html'), name='MatchSelect'),
    url(r'^gameview/$', views.GameView.as_view(template_name='matchview.html'), name='GameView'),
    # selecting a sport
    #url(r'^selectsport/$', views.SelectSport.as_view(template_name='selectsport.html'), name='SelectSport'),
    url(r'^sportview/$', views.SportView.as_view(template_name='sportview.html'), name='SportView'),
    # selecting a school
    #url(r'^selectschool/$', views.SelectSchool.as_view(template_name='selectschool.html'), name='SelectSchool'),
    url(r'^schoolview/$', views.SchoolView.as_view(template_name='schoolview.html'), name='SchoolView'),
    #update scores
    url(r'^reportscore/$', views.ScoreReport.as_view(template_name='reportscore.html'), name='ScoreReport'),
    url(r'^coachview/$', views.CoachView.as_view(template_name='coachview.html'), name='CoachView'),
    url(r'^editteam/$', views.EditTeam.as_view(template_name='editteam.html'), name='EditTeam'),
    url(r'^home/$', views.HomeView.as_view(template_name='homeview.html'), name='HomeView'),
    #adding pictures
    url(r'^addpic/$', views.AddPic.as_view(template_name='addpic.html'), name='AddPic'),
    url(r'^mypic/$', views.MyPic.as_view(template_name='mypic.html'), name='MyPic'),
    url(r'^(?P<pk>[0-9]+)/delete/$',views.DeletePic.as_view(),name='DeletePic'),
]