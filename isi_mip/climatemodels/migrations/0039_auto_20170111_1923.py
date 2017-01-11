# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 18:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climatemodels', '0038_inputdatainformation_otherinformation_technicalinformation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impactmodel',
            name='additional_input_data_sets',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='anything_else',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='climate_data_sets',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='climate_variables',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='climate_variables_info',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='exceptions_to_protocol',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='extreme_events',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='management',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='natural_vegetation_cover_dataset',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='natural_vegetation_dynamics',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='natural_vegetation_partition',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='socioeconomic_input_variables',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='soil_dataset',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='spatial_aggregation',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='spatial_resolution',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='spatial_resolution_info',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='spin_up',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='spin_up_design',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='temporal_resolution_climate',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='temporal_resolution_co2',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='temporal_resolution_info',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='temporal_resolution_land',
        ),
        migrations.RemoveField(
            model_name='impactmodel',
            name='temporal_resolution_soil',
        ),
    ]
