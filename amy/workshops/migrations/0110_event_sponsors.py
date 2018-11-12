# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-03 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0109_add_sponsorship_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sponsors',
            field=models.ManyToManyField(blank=True, related_name='sponsored_events', through='workshops.Sponsorship', to='workshops.Host'),
        ),
    ]