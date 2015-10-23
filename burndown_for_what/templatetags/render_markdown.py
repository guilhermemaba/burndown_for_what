# -*- coding: utf8 -*-
# vim: ts=4 sts=4 sw=4 et:

import markdown
from django import template

register = template.Library()


@register.filter
def markdownify(text):
    return markdown.markdown(
        text,
        extensions=['markdown.extensions.tables'],
        safe_mode='escape'
    )
