# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0036_auto_20170111_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactmodel',
            name='name',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='owners',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='region',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='sector',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='short_description',
        ),
    ]
