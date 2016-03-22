# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model('contenttypes.ContentType')
    Page = apps.get_model('wagtailcore.Page')
    Site = apps.get_model('wagtailcore.Site')
    HomePage = apps.get_model('pages.HomePage')
    # Delete the default homepage
    Page.objects.get(id=2).delete()

    # Create content type for homepage model
    homepage_content_type, created = ContentType.objects.get_or_create(
        model='homepage', app_label='pages')

    # Create a new homepage
    homepage = HomePage.objects.create(
        title="Homepage",
        slug='home',
        content_type=homepage_content_type,
        path='00010001',
        depth=2,
        numchild=0,
        url_path='/home/',
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(
        hostname='localhost', root_page=homepage, is_default_site=True)

    return homepage
    # import ipdb; ipdb.set_trace()

def create_pages(apps, schema_editor):
    homepage = create_homepage(apps, schema_editor)
    ContentType = apps.get_model('contenttypes.ContentType')

    FAQPage = apps.get_model('pages.FAQPage')
    faqpage_content_type, created = ContentType.objects.get_or_create(
        model='homepage', app_label='pages')
    FAQPage.objects.create(
        title="FAQ",
        slug='faq',
        content_type=faqpage_content_type,
        path='000100010001',
        depth=3,
        numchild=0,
        url_path='/home/faq/')
    homepage.numchild=1
    homepage.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_pages),
    ]
