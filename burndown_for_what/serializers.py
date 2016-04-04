# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from rest_framework import serializers

from burndown_for_what.models import Sprint, Issue


class MilestoneGithubSerializer(serializers.BaseSerializer):
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


class IssueGithubSerializer(serializers.BaseSerializer):
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


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ('id', 'name', 'team', 'date_begin', 'score', 'closed', 'sprint_scored')


class SprintCustomSerializer(serializers.ModelSerializer):
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
