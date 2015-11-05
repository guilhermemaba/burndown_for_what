# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from django.contrib import admin
from burndown_for_what.models import Organization, Team, Sprint, Daily


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class DailyInline(admin.TabularInline):
    extra = 0
    model = Daily
    raw_id_fields = ('sprint',)

    fieldsets = (
        ('', {
            'fields': ('date', 'score', 'score_unplanned', 'observation', 'closed',)
        }),
    )

    class Meta:
        model = Daily


class SprintAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'scrum_master', 'score', 'sprint_scored', 'score_unplanned', 'closed')
    list_filter = ('team__name', 'closed', 'scrum_master__username')
    search_fields = ('team__name', 'closed', 'scrum_master__usernname')
    inlines = (DailyInline,)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Sprint, SprintAdmin)
