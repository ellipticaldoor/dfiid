# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noty',
            name='description',
        ),
        migrations.RemoveField(
            model_name='noty',
            name='post',
        ),
        migrations.AlterField(
            model_name='noty',
            name='category',
            field=models.CharField(choices=[('C', 'commit'), ('F', 'follow')], max_length=2),
        ),
    ]
