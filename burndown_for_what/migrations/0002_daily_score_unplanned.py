# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burndown_for_what', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily',
            name='score_unplanned',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
