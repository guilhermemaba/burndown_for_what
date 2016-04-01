# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

from pygithub3 import Github

from django.conf import settings


SPRINT_POINT = ['0.5', '1', '2', '3', '5', '8', '13', '21']


def connect_github(user=None, repo=None):
    """
    Create connection with GitHub.

    :param str user:
    :param str repo:
    :return GitHub:
    """
    data = settings.GITHUB_DATA
    return Github(
        login=data.get('login'),
        password=data.get('password'),
        user=user or data.get('user'),
        repo=repo or data.get('repo')
    )
