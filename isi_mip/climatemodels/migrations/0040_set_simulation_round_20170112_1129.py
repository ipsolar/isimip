# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 10:29
from __future__ import unicode_literals

from django.db import migrations


def set_simulation_round(apps, schema_editor):
    ImpactModel = apps.get_model('climatemodels', 'ImpactModel')
    SimulationRoundModel = apps.get_model('climatemodels', 'SimulationRound')
    isimip2a = SimulationRoundModel.objects.get(name="ISIMIP2a")
    ImpactModel.objects.filter(simulation_round=None).update(simulation_round=isimip2a)


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0039_auto_20170111_1923'),
    ]

    operations = [
        migrations.RunPython(
            set_simulation_round
        ),
    ]
