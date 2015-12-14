# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from django.views.generic import ListView, TemplateView
from burndown_for_what.models import Sprint


class SprintListView(ListView):
    model = Sprint
    template_name = 'sprint/list.html'

    def get_context_data(self, **kwargs):
        context = super(SprintListView, self).get_context_data(**kwargs)
        context['sprints'] = 'active'

        return context


class BurndownTemplateView(TemplateView):
    template_name = 'sprint/burndown.html'

    def get_context_data(self, **kwargs):
        sprint = Sprint.objects.get(pk=kwargs.get('sprint_id'))
        context = super(BurndownTemplateView, self).get_context_data(**kwargs)
        context['sprints'] = 'active'

        context['team'] = sprint.team.name
        context['name'] = sprint.name
        context['resume'] = sprint.resume
        context['yticks'] = sprint.get_ticks()
        context['burndown_data'] = sprint.get_data_burndown()
        return context
