# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from django.conf.urls import url
from django.views.generic import TemplateView
from burndown_for_what.views import BurndownTemplateView, SprintListView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='burndown.html'), name='home'),
    url(r'^sprint/$', SprintListView.as_view(), name='sprint_list'),
    url(
        r'^sprint/(?P<sprint_id>\d+)/$',
        BurndownTemplateView.as_view(),
        name='burndown_sprint'
    ),
]
