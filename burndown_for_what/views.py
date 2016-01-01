# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:
from django.conf import settings

from collections import defaultdict
from itertools import groupby

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse

from pygithub3 import Github

from burndown_for_what.models import Sprint, Daily


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


class ImportTemplateView(TemplateView):
    template_name = 'import.html'

    def _connect_github(self):
        data = settings.GITHUB_DATA
        return Github(
            login=data.get('login'), password=data.get('password'),
            user=data.get('user'), repo=data.get('repo')
        )

    def _get_last_sprint(self, gh):
        """ Get the sprint with latest end """
        for sprint in gh.issues.milestones.list(sort='due_date').all():
            # Get the last sprint by due_date
            if sprint.title.startswith('Sprint'):
                return sprint
        return None

    def _get_closed_issues(self, gh, sprint):
        return gh.issues.list_by_repo(milestone=sprint.number, state='closed').all()

    def check_labels(self, issue):
        is_planned, score = True, 0
        for label in issue.labels:
            try:
                score = float(label.name)
            except ValueError:
                if label.name == 'unplanned':
                    is_planned = False
        return is_planned, score

    def _scores_by_day(self, issues):
        closed_issues = groupby(
            sorted(issues, key=lambda x: x.closed_at), lambda x: x.closed_at.date()
        )
        day_issues = defaultdict(dict)

        for date, issues in closed_issues:
            date_key = date.strftime("%Y-%m-%d")
            day_issues[date_key] = defaultdict(int)
            for issue in list(issues):
                is_planned, scores = self.check_labels(issue)
                day_issues[date_key]['planned' if is_planned else 'unplanned'] += scores

        return day_issues

    def get_context_data(self, **kwargs):
        context = super(ImportTemplateView, self).get_context_data(**kwargs)
        gh_conn = self._connect_github()

        sprint = self._get_last_sprint(gh_conn)
        issues = self._get_closed_issues(gh_conn, sprint)
        scores = self._scores_by_day(issues)

        self.request.session['scores'] = dict(scores)
        context['sprint_title'] = sprint.title
        context['scores'] = dict(scores)

        return context


class ImportView(View):

    def post(self, *args, **kwargs):
        try:
            sprint = Sprint.objects.last()
            days = self.request.POST.getlist('days')

            for day, score in self.request.session['scores'].iteritems():
                if day in days:
                    Daily.objects.create(date=day, score=score.get('planned'),
                        score_unplanned=score.get('unplanned'), closed=True,
                        sprint=sprint).save()

        except KeyError:
            raise Exception('No data selected')

        return HttpResponseRedirect(reverse('burndown_sprint', args=(sprint.id,)))
