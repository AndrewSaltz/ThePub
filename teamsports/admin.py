from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import School, Teams, Schedule, ScheduleAdmin, Photo, GameNotes, Profile, Info
from .models import Sports
admin.site.register(School)
admin.site.register(Sports)
admin.site.register(Teams)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Photo)
admin.site.register(GameNotes)
admin.site.register(Profile)
admin.site.register(Info)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

