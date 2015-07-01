# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import core.core
import content.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('commitid', models.CharField(primary_key=True, serialize=False, default=core.core._createId, max_length=16)),
                ('body', models.TextField(default='', max_length=500)),
                ('body_html', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('show', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('postid', models.CharField(primary_key=True, serialize=False, default=core.core._createId, max_length=16)),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('body', models.TextField(max_length=3000)),
                ('body_html', models.TextField(null=True, blank=True)),
                ('image', django_resized.forms.ResizedImageField(null=True, upload_to=content.models.Post.get_image, blank=True)),
                ('draft', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_commited', models.DateTimeField(null=True)),
                ('commit_number', models.IntegerField(default=0)),
                ('show', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sub',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False, max_length=10)),
                ('image', models.ImageField(upload_to=content.models.Sub.get_image)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_commited', models.DateTimeField(auto_now_add=True)),
                ('follower_number', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-last_commited'],
            },
        ),
        migrations.CreateModel(
            name='SubFollow',
            fields=[
                ('sub_followid', models.CharField(primary_key=True, serialize=False, blank=True, max_length=33)),
            ],
        ),
    ]
