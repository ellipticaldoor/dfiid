# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.SlugField(primary_key=True, serialize=False, max_length=16)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_commited', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('avatar', models.ImageField(upload_to=user.models.User.get_avatar)),
                ('cover', models.ImageField(null=True, upload_to=user.models.User.get_cover, blank=True)),
                ('follower_number', models.IntegerField(default=0)),
                ('following_number', models.IntegerField(default=0)),
                ('sub_following_number', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_query_name='user', verbose_name='groups', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', blank=True, related_query_name='user', verbose_name='user permissions', related_name='user_set')),
            ],
            options={
                'ordering': ['-last_commited'],
            },
        ),
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('followid', models.CharField(primary_key=True, serialize=False, blank=True, max_length=33)),
                ('followed', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='followed')),
                ('follower', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='follower')),
            ],
        ),
    ]
