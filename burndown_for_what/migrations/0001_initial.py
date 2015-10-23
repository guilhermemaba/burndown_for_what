# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('score', models.FloatField(blank=True, null=True)),
                ('observation', models.TextField(blank=True, null=True)),
                ('closed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('resume', models.TextField(blank=True, help_text='Markdown is possible.', null=True)),
                ('date_begin', models.DateField()),
                ('score', models.FloatField()),
                ('notify_daily', models.BooleanField(default=True)),
                ('notify_closed', models.BooleanField(default=True)),
                ('closed', models.BooleanField()),
                ('scrum_master', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('persons', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='sprint',
            name='team',
            field=models.ForeignKey(to='burndown_for_what.Team'),
        ),
        migrations.AddField(
            model_name='daily',
            name='sprint',
            field=models.ForeignKey(to='burndown_for_what.Sprint'),
        ),
    ]
