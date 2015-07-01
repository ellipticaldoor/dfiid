# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.core
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20150605_1150'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_user_noty_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noty',
            fields=[
                ('notyid', models.CharField(primary_key=True, default=core.core._createId, max_length=16, serialize=False)),
                ('category', models.CharField(choices=[('P', 'post'), ('C', 'commit'), ('F', 'follow')], max_length=2)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('show', models.BooleanField(default=True)),
                ('commit', models.ForeignKey(blank=True, null=True, to='content.Commit', related_name='notys_post')),
                ('follow', models.ForeignKey(blank=True, null=True, to='user.UserFollow', related_name='notys_follow')),
                ('post', models.ForeignKey(blank=True, null=True, to='content.Post', related_name='notys_post')),
                ('user', models.ForeignKey(related_name='notys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
