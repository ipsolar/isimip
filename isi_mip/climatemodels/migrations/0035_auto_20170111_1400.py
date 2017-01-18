# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 13:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def move_data_to_base_impact_model(apps, schema_editor):
    ImpactModel = apps.get_model('climatemodels', 'ImpactModel')
    BaseImpactModel = apps.get_model('climatemodels', 'BaseImpactModel')

    SimulationRoundModel = apps.get_model('climatemodels', 'SimulationRound')
    fast_track = SimulationRoundModel.objects.get_or_create(name="Fast Track")
    fast_track.order = 1
    fast_track.save()
    isimip2a = SimulationRoundModel.objects.get_or_create(name="ISIMIP2a")
    isimip2a.order = 2
    isimip2a.save()
    for impact_model in ImpactModel.objects.all():
        # do your data migration here
        base = BaseImpactModel.objects.create(
            name=impact_model.name,
            sector=impact_model.sector,
            short_description=impact_model.short_description,
        )
        base.region = impact_model.region.all()
        base.owners = impact_model.owners.all()
        base.save()
        impact_model.base_model = base
        if impact_model.simulation_round.exists():
            impact_model.simulation_round_new = impact_model.simulation_round.all().order_by("-order")[0]
        impact_model.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('climatemodels', '0034_auto_20170111_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseImpactModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('sector', models.CharField(choices=[('Agriculture', 'Agriculture'), ('Agro-Economic Modelling', 'Agro-Economic Modelling'), ('Biodiversity', 'Biodiversity'), ('Biomes', 'Biomes'), ('Coastal Infrastructure', 'Coastal Infrastructure'), ('Computable General Equilibrium Modelling', 'Computable General Equilibrium Modelling'), ('Energy', 'Energy'), ('Forests', 'Forests'), ('Health', 'Health'), ('Marine Ecosystems and Fisheries (global)', 'Marine Ecosystems and Fisheries (global)'), ('Marine Ecosystems and Fisheries (regional)', 'Marine Ecosystems and Fisheries (regional)'), ('Permafrost', 'Permafrost'), ('Water (global)', 'Water (global)'), ('Water (regional)', 'Water (regional)')], help_text='The sector to which this information pertains. Some models may have further entries for other sectors.', max_length=500)),
                ('short_description', models.TextField(blank=True, help_text='This short description should assist other researchers in briefly describing the model in a paper.', null=True, verbose_name='Short model description')),
                ('owners', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('region', models.ManyToManyField(help_text='Region for which model produces results', to='climatemodels.Region')),
            ],
        ),
        migrations.AddField(
            model_name='impactmodel',
            name='simulation_round_new',
            field=models.ForeignKey(blank=True, help_text='The ISIMIP simulation round for which these model details are relevant', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='simulation_round_new', to='climatemodels.SimulationRound'),
        ),
        migrations.AddField(
            model_name='impactmodel',
            name='base_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='base_model', to='climatemodels.BaseImpactModel'),
        ),
        # save old data before removing fields
        migrations.RunPython(
            move_data_to_base_impact_model
        ),
    ]
