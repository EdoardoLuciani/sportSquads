from django.contrib import admin
from sportSquads.models import *

class TeamUserMembershipInline(admin.TabularInline):
    model = TeamUserMembership
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    inlines = (TeamUserMembershipInline,)

class TeamAdmin(admin.ModelAdmin):
    inlines = (TeamUserMembershipInline,)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Sport)
admin.site.register(Team, TeamAdmin)

