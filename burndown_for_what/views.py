# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.generic import TemplateView

from burndown_for_what.models import Sprint
from burndown_for_what.utils import connect_github
from burndown_for_what.serializers import (
    MilestoneGithubSerializer,
    IssueModelSerializer,
    IssueGithubSerializer,
    SprintCustomSerializer,
    SprintSerializer,
)


class BurndownTemplateView(TemplateView):
    template_name = 'burndown.html'

    def get_context_data(self, **kwargs):
        sprint = Sprint.objects.get(pk=kwargs.get('sprint_id'))
        context = super(BurndownTemplateView, self).get_context_data(**kwargs)
        context['team'] = sprint.team.name
        context['issues'] = sprint.issue_set.filter(unplanned=False).order_by('-state', 'assignee_login')
        context['issues_unplanned'] = sprint.issue_set.filter(unplanned=True).order_by('-state', 'assignee_login')
        context['name'] = sprint.name
        context['resume'] = sprint.resume
        context['yticks'] = sprint.get_ticks()
        context['burndown_data'] = sprint.get_data_burndown()
        return context


class SprintView(generics.ListAPIView):
    model = Sprint
    serializer_class = SprintSerializer

    def get_queryset(self):
        # TODO create filters
        return Sprint.objects.all()


class SprintDetailView(APIView):
    model = Sprint
    serializer_class = SprintCustomSerializer

    def get(self, request, sprint_id):
        serializer = self.serializer_class(Sprint.objects.get(id=sprint_id))
        return Response(serializer.data)


class MilestoneView(generics.ListAPIView):
    """
    Search milestone on GitHub.
    """
    serializer_class = MilestoneGithubSerializer

    def get_queryset(self):
        # FIXME 2x
        connection = connect_github()
        return connection.issues.milestones.list(sort='due_date').all()


class IssueView(generics.ListAPIView):
    """
    Search issue on GitHub.
    """
    serializer_class = IssueGithubSerializer

    def get_queryset(self):
        # FIXME 2x
        connection = connect_github()
        return connection.issues.list_by_repo(state='all', **self.kwargs).all()
