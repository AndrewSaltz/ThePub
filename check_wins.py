import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thepub.settings")
django.setup()

#Get models
from teamsports.models import Teams, Schedule

#Get F
from django.db.models import F

#Make all wins, losses, ties at zero
Teams.objects.all().update(loss=0, win=0, tie=0)

#The logic, practice
for games in Schedule.objects.all():
    if games.is_disputed is False:
        if games.home_score is not None and games.away_score is not None:
            if games.home_score > games.away_score:
                winner = Teams.objects.get(pk=games.home.team)
                loser = Teams.objects.get(pk=games.away.team)
                winner.win = F('win') + 1
                loser.loss = F('loss') +1
                winner.save()
                loser.save()
                print (winner)
            elif games.home_score < games.away_score:
                winner = Teams.objects.get(pk=games.away.team)
                loser = Teams.objects.get(pk=games.home.team)
                winner.win = F('win') + 1
                loser.loss = F('loss') +1
                winner.save()
                loser.save()
                print (winner)
            elif games.home_score == games.away_score:
                home_tie = Teams.objects.get(pk=games.away.team)
                away_tie = Teams.objects.get(pk=games.home.team)
                home_tie.tie = F('tie') + 1
                away_tie.tie = F('tie') +1
                home_tie.save()
                away_tie.save()
                print ("tie")
        else:
            pass
    else:
        continue
