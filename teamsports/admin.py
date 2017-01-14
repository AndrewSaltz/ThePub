from django.contrib import admin

# Register your models here.
from .models import School, Teams, Schedule, ScheduleAdmin, Photo, GameNotes
from .models import Sports
admin.site.register(School)
admin.site.register(Sports)
admin.site.register(Teams)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Photo)
admin.site.register(GameNotes)
