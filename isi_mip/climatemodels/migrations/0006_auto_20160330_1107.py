# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-30 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0005_auto_20160330_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impactmodel',
            name='other_references',
            field=models.ManyToManyField(blank=True, to='climatemodels.ReferencePaper'),
        ),
        migrations.AlterField(
            model_name='impactmodel',
            name='simulation_round',
            field=models.ManyToManyField(blank=True, help_text='For which ISIMIP simulation round are these model details relevant?', to='climatemodels.SimulationRound'),
        ),
    ]
