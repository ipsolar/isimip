# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-19 09:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0048_delete_wrong_variables'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inputdata',
            old_name='scenario',
            new_name='old_scenario',
        ),
        migrations.RenameField(
            model_name='inputdata',
            old_name='simulation_round',
            new_name='old_simulation_round',
        ),
    ]
