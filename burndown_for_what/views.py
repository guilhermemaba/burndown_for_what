# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from rest_framework import serializers, generics

from django.views.generic import TemplateView

from burndown_for_what.models import Sprint
from burndown_for_what.models import connect_github


class BurndownTemplateView(TemplateView):
    template_name = 'burndown.html'

    def get_context_data(self, **kwargs):
        sprint = Sprint.objects.get(pk=kwargs.get('sprint_id'))
        context = super(BurndownTemplateView, self).get_context_data(**kwargs)
        context['team'] = sprint.team.name
        context['name'] = sprint.name
        context['resume'] = sprint.resume
        context['yticks'] = sprint.get_ticks()
        context['burndown_data'] = sprint.get_data_burndown()
        return context


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ('id', 'name', 'team', 'date_begin', 'score', 'closed', 'sprint_scored')


class MilestoneSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'title': obj.title,
            'description': obj.description,
            'url': obj.url,
            'number': obj.number,
            'state': obj.state,
            'due_on': obj.due_on,
            'closed_at': obj.closed_at,
        }


class IssueSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        assignee = obj.assignee
        return {
            'id': obj.id,
            'title': obj.title,
            'url': obj.url,
            'number': obj.number,
            'state': obj.state,
            'closed_at': obj.closed_at,
            'created_at': obj.created_at,
            'labels': [label.name for label in obj.labels],
            'assignee': {
                'id': assignee.id,
                'login': assignee.login,
                'url': assignee.url,
                'avatar_url': assignee.avatar_url,
            },
        }


class SprintView(generics.ListAPIView):
    model = Sprint
    serializer_class = SprintSerializer

    def get_queryset(self):
        # TODO create filters
        return Sprint.objects.all()


class MilestoneView(generics.ListAPIView):
    serializer_class = MilestoneSerializer

    def get_queryset(self):
        # FIXME 2x
        connection = connect_github()
        return connection.issues.milestones.list(sort='due_date').all()


class IssueView(generics.ListAPIView):
    serializer_class = IssueSerializer

    def get_queryset(self):
        # FIXME 2x
        connection = connect_github()
        return connection.issues.list_by_repo(state='all', **self.kwargs).all()
