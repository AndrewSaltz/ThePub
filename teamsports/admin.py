from django.contrib import admin

# Register your models here.
from .models import School, Teams, Schedule, ScheduleAdmin, TeamsAdmin
from .models import Sports
admin.site.register(School)
admin.site.register(Sports)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Schedule, ScheduleAdmin)
