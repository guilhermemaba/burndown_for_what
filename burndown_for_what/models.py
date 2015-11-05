# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from django.db import models


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
    score = models.FloatField()
    notify_daily = models.BooleanField(default=True)
    notify_closed = models.BooleanField(default=True)
    closed = models.BooleanField()

    def __str__(self):
        return u'{}'.format(self.name)

    def _get_max_score(self):
        return int(self.score + 2)

    def get_ticks(self):
        return [tick for tick in range(self._get_max_score())]

    @property
    def duration(self):
        return self.daily_set.count()

    @property
    def score_unplanned(self):
        dailys = self.daily_set.all()
        if dailys:
            return sum([daily.score_unplanned for daily in dailys if daily.score_unplanned])
        return 0

    @property
    def sprint_scored(self):
        dailys = self.daily_set.all()
        if dailys:
            return sum([daily.score for daily in dailys if daily.score])
        return 0

    def get_data_burndown(self):
        # FIXME refactor this method
        score_per_day = self.score/self.duration
        score_daily = 0
        score_unplanned = 0
        result = [(str(self.date_begin), self.score, self.score, 0),]

        for x, daily in enumerate(self.daily_set.all(), start=1):
            burndown_daily_score = self.score - (x * score_per_day)
            score_daily += daily.score if daily.score else 0
            score_unplanned += daily.score_unplanned if daily.score_unplanned else 0
            if daily.closed:
                score_team = (self.score-score_daily)
                result.append(
                    (str(daily.date), score_team, burndown_daily_score, score_unplanned)
                )
            else:
                result.append(
                    (str(daily.date), None, burndown_daily_score, None)
                )

        return result


class Daily(models.Model):
    sprint = models.ForeignKey('burndown_for_what.Sprint')
    date = models.DateField()
    score = models.FloatField(null=True, blank=True)
    score_unplanned = models.FloatField(null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    closed = models.BooleanField()

    def __str__(self):
        return u'{}'.format(self.date)
