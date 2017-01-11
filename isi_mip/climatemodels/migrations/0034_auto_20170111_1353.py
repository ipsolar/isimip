# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 12:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0033_auto_20160713_1004'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='simulationround',
            options={'ordering': ('-order',)},
        ),
        migrations.RemoveField(
            model_name='inputdata',
            name='phase',
        ),
        migrations.AddField(
            model_name='inputdata',
            name='simulation_round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='climatemodels.SimulationRound'),
        ),
        migrations.AddField(
            model_name='simulationround',
            name='order',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='InputPhase',
        ),
    ]
