# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from django.db import models

from burndown_for_what.utils import SPRINT_POINT, connect_github


class Organization(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return u'{}'.format(self.name)


class Team(models.Model):
    name = models.CharField(max_length=150)
    persons = models.ManyToManyField('auth.User')

    def __str__(self):
        return u'{}'.format(self.name)


class Sprint(models.Model):
    name = models.CharField(max_length=150)
    scrum_master = models.ForeignKey('auth.User')
    team = models.ForeignKey('burndown_for_what.Team')
    resume = models.TextField(null=True, blank=True, help_text=u'Markdown is possible.')
    date_begin = models.DateField()
    github_user = models.CharField(max_length=150, blank=True, null=True)
    github_repo = models.CharField(max_length=150, blank=True, null=True)
    github_milestone_id = models.IntegerField(default=0)
    closed = models.BooleanField()

    def __str__(self):
        return u'{}'.format(self.name)

    def _update_daily(self):
        issues_closed = self.issue_set.filter(state='closed')
        for daily in self.daily_set.all():
            issues_daily = issues_closed.filter(closed_at=daily.date)
            if issues_daily:
                daily.score = sum(issues_daily.filter(unplanned=False).values_list('score', flat=True))
                daily.score_unplanned = sum(issues_daily.filter(unplanned=True).values_list('score', flat=True))
                daily.save()

    def _create_issue(self, issue):
        """
        Create model Issues with data from GitHub.

        :param Issue issue:
        :return:
        """
        unplanned = any([label for label in issue.labels if label.name == 'unplanned'])
        score = sum([float(label.name) for label in issue.labels if label.name in SPRINT_POINT])
        Issue.objects.create(
            sprint=self,
            title=issue.title,
            github_id=issue.id,
            url=issue.html_url,
            number=issue.number,
            state=issue.state,
            assignee_login=issue.assignee.login,
            closed_at=issue.closed_at,
            score=score,
            unplanned=unplanned
        )

    def save(self, *args, **kwargs):
        """
        Save object and search/create issues refers the milestone, after this, update *dailys*

        :return:
        """
        connection = connect_github(self.github_user, self.github_repo)
        Issue.objects.filter(sprint=self).delete()
        super(Sprint, self).save(*args, **kwargs)
        for issue in connection.issues.list_by_repo(state='all', **{'milestone': self.github_milestone_id}).all():
            self._create_issue(issue)
        self._update_daily()

    @property
    def duration(self):
        return self.daily_set.count()

    @property
    def score_unplanned(self):
        return sum(self.issue_set.filter(unplanned=True, state='closed').values_list('score', flat=True))

    @property
    def scored(self):
        return sum(self.issue_set.filter(unplanned=False, state='closed').values_list('score', flat=True))

    @property
    def score(self):
        return sum(self.issue_set.filter(unplanned=False).values_list('score', flat=True))

    @property
    def issues_count(self):
        return self.issue_set.count()

    @property
    def avg_score(self):
        return self.score / self.duration

    @staticmethod
    def burndown_point(score, index, avg_score):
        return score - (index * avg_score)

    def chart_data(self):
        """
        Returns need data for ploting chart.

        :return dict:
        """
        # create local variables for avoid hints on Database.
        score = self.score
        score_daily = 0
        score_unplanned = 0
        score_per_day = self.avg_score

        result = {
            'days': [self.date_begin,],
            'burndown_line': [score,],
            'score': [score,],
            'unplanned': [0,],
        }
        for x, daily in enumerate(self.daily_set.all(), start=1):
            result['days'].append(str(daily.date))
            result['burndown_line'].append(Sprint.burndown_point(score, x, score_per_day))
            if daily.closed:
                score_unplanned += daily.score_unplanned if daily.score_unplanned else 0
                score_daily += daily.score if daily.score else 0
                result['score'].append(score - score_daily)
                result['unplanned'].append(score_unplanned)
        return result


class Issue(models.Model):
    sprint = models.ForeignKey('burndown_for_what.Sprint')
    title = models.TextField()
    github_id = models.IntegerField(default=0)
    url = models.TextField()
    number = models.IntegerField(default=0)
    state = models.CharField(max_length=150, blank=True, null=True)
    assignee_login = models.CharField(max_length=150, blank=True, null=True)
    closed_at = models.DateField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    unplanned = models.NullBooleanField()


class Daily(models.Model):
    sprint = models.ForeignKey('burndown_for_what.Sprint')
    date = models.DateField()
    score = models.FloatField(null=True, blank=True)
    score_unplanned = models.FloatField(null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    closed = models.BooleanField()

    def __str__(self):
        return u'{}'.format(self.date)
