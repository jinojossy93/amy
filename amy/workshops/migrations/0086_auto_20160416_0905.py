# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-16 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0085_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='repository_last_commit_hash',
            field=models.CharField(blank=True, default='', help_text="Event's repository last commit SHA1 hash", max_length=40),
        ),
        migrations.AddField(
            model_name='event',
            name='repository_tags',
            field=models.TextField(blank=True, default='', help_text="JSON-serialized tags from event's website"),
        ),
        migrations.AddField(
            model_name='event',
            name='tag_changes_detected',
            field=models.TextField(blank=True, default='', help_text='List of detected tag changes'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags_changed',
            field=models.BooleanField(default=False, help_text='Indicate if tags changed since last check'),
        ),
    ]
