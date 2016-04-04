# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from rest_framework import serializers, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.generic import TemplateView

from burndown_for_what.models import Sprint, Issue
from burndown_for_what.utils import connect_github


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


class IssueModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class SprintModelSerializer(serializers.ModelSerializer):
    issues = serializers.SerializerMethodField()
    burndown_data = serializers.SerializerMethodField()
    team = serializers.ReadOnlyField(source='team.name')
    scrum_master = serializers.ReadOnlyField(source='scrum_master.username')

    class Meta:
        model = Sprint
        fields = ('name', 'scrum_master', 'team', 'date_begin', 'score', 'github_user', 'github_repo',
                  'github_milestone_id', 'closed', 'issues', 'burndown_data',
        )

    def get_burndown_data(self, sprint):
        return sprint.get_data_burndown()

    def get_issues(self, sprint):
        serializer = IssueModelSerializer(instance=sprint.issue_set.all(),  many=True)
        return serializer.data


class SprintView(generics.ListAPIView):
    model = Sprint
    serializer_class = SprintSerializer

    def get_queryset(self):
        # TODO create filters
        return Sprint.objects.all()


class SprintDetailView(APIView):
    model = Sprint
    serializer_class = SprintModelSerializer

    def get(self, request, sprint_id):
        serializer = self.serializer_class(Sprint.objects.get(id=sprint_id))
        return Response(serializer.data)


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
