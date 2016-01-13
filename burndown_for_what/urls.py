# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from django.conf.urls import include, url
from django.contrib import admin
from burndown_for_what.views import BurndownTemplateView, ImportTemplateView, ImportView, SprintView, MilestoneView, IssueView


urlpatterns = [
    url(
        r'^sprint/(?P<sprint_id>\d+)/$',
        BurndownTemplateView.as_view(),
        name='burndown_sprint'
    ),
    url(
        r'^import/$',
        ImportTemplateView.as_view(),
        name='import'
    ),
    url(
        r'^daily/$',
        ImportView.as_view(),
        name='daily_save'
    ),
    url(
        r'^api/sprint/$',
        SprintView.as_view(),
        name='api_sprint'
    ),
    url(
        r'^api/milestones/$',
        MilestoneView.as_view(),
        name='api_milestones'
    ),
    url(
        r'^api/issues/(?P<milestone>\w+)/$',
        IssueView.as_view(),
        name='api_milestones'
    ),
]
