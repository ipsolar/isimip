# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 11:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('climatemodels', '0029_auto_20160620_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='impactmodel',
            name='owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='impactmodel',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
