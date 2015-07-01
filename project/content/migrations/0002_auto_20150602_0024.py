# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subfollow',
            name='follower',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sub_follower'),
        ),
        migrations.AddField(
            model_name='subfollow',
            name='sub',
            field=models.ForeignKey(to='content.Sub', related_name='sub_followed'),
        ),
        migrations.AddField(
            model_name='post',
            name='sub',
            field=models.ForeignKey(to='content.Sub', related_name='posts'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='posts'),
        ),
        migrations.AddField(
            model_name='commit',
            name='post',
            field=models.ForeignKey(to='content.Post', related_name='commits'),
        ),
        migrations.AddField(
            model_name='commit',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='commits'),
        ),
    ]
