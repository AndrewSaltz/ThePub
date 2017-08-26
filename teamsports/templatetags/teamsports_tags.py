from django import template
from teamsports.models import Photo, GameNotes, Schedule, Profile
from django.db.models import Q
from datetime import datetime
from django.shortcuts import render_to_response

register = template.Library()

@register.filter
def next_game(value):
    now = datetime.now().date()
    next = Schedule.objects.filter(Q(home=value) | Q(away=value)).filter(match_date__gt=now).order_by('match_date').first()
    if next == None:
        next = "No games scheduled!"
    else:
        return next

    return next

@register.simple_tag
def game_day(user):
    if user.groups.filter(name__in=['Coach', 'Reporter', 'Admin']).exists():
        profile = Profile.objects.get(user=user).team
        if profile == None:
            return False
        else:
            profile = profile.team
            now = datetime.now()
            is_game = Schedule.objects.filter(Q(home=profile) | Q(away=profile)).filter(match_date__year=now.year).filter(match_date__month=now.month).filter(match_date__day=now.day)
            if is_game.exists():
                return True
            else:
                return False
    else:
        return False

@register.inclusion_tag('coachview.html')
def game_alert(request, game_alert):
    profile = Profile.objects.get(user=request.user)
    now = datetime.now()
    game_alert = Schedule.objects.filter(Q(home=profile) | Q(away=profile)).filter(match_date__year=now.year).filter(match_date__month=now.month).filter(match_date__day=now.day)
    return render_to_response ("coachview.html", game_alert)

@register.simple_tag
def get_obj(pk, attr):
    obj = getattr(Photo.objects.get(pk=int(pk)), attr)
    return obj

@register.filter
def get_pic(value):
    value = Photo.objects.get(pk=value).photo.thumbnail['400x400'].url
    return value

@register.filter
def pic_game(value):
    value = Photo.objects.get(pk=value).game.match
    return value

@register.filter
def get_notes_game(value):
    value = GameNotes.objects.get(pk=value)
    return value

@register.filter
def get_score(value):
    value = Schedule.objects.get(pk=value)
    return value

@register.filter
def data_verbose(boundField):
    """
    Returns field's data or it's verbose version
    for a field with choices defined.

    Usage::

        {% load data_verbose %}
        {{form.some_field|data_verbose}}
    """
    data = boundField.data
    field = boundField.field
    return hasattr(field, 'choices') and dict(field.choices).get(data,'') or data