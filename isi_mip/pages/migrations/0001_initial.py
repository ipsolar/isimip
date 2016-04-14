# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 07:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import isi_mip.contrib.blocks
import isi_mip.pages.blocks
import modelcluster.fields
import wagtail.contrib.wagtailroutablepage.models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0008_auto_20160401_1645'),
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.StreamField((('columns_1_to_1', wagtail.wagtailcore.blocks.StructBlock((('left_column', wagtail.wagtailcore.blocks.StreamBlock((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))))), ('right_column', wagtail.wagtailcore.blocks.StreamBlock((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))), form_classname='pull-right'))))), ('columns_1_to_2', wagtail.wagtailcore.blocks.StructBlock((('left_column', wagtail.wagtailcore.blocks.StreamBlock((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))))), ('right_column', wagtail.wagtailcore.blocks.StreamBlock((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))), form_classname='pull-right'))))), ('columns_2_to_1', wagtail.wagtailcore.blocks.StructBlock((('left_column', wagtail.wagtailcore.blocks.StreamBlock((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))))), ('right_column', wagtail.wagtailcore.blocks.StreamBlock((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))), form_classname='pull-right'))))), ('image', isi_mip.pages.blocks.ImageBlock()), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock())))), ('paper', wagtail.wagtailcore.blocks.StructBlock((('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('author', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('journal', wagtail.wagtailcore.blocks.CharBlock()), ('link', wagtail.wagtailcore.blocks.URLBlock())), template='widgets/page-teaser-wide.html')), ('bigteaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False)))))))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('blogindexpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.BlogIndexPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogindexpage',),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('blogpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.BlogPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogpage',),
        ),
        migrations.CreateModel(
            name='DashboardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FAQPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.StreamField((('columns_1_to_1', wagtail.wagtailcore.blocks.StructBlock((('left_column', wagtail.wagtailcore.blocks.StreamBlock((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))))), ('right_column', wagtail.wagtailcore.blocks.StreamBlock((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))), form_classname='pull-right'))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', wagtail.wagtailcore.blocks.RichTextBlock()))))))))))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to this address', max_length=255, verbose_name='to address')),
                ('from_address', models.CharField(blank=True, max_length=255, verbose_name='from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='subject')),
                ('confirmation_text', models.TextField(default='Your registration was submitted')),
                ('top_content', wagtail.wagtailcore.fields.StreamField((('richtext', wagtail.wagtailcore.blocks.RichTextBlock()),))),
                ('bottom_content', wagtail.wagtailcore.fields.StreamField((('richtext', wagtail.wagtailcore.blocks.RichTextBlock()),))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='GettingStartedPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.StreamField((('input_data', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()),))), ('contact', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()), ('sectors', wagtail.wagtailcore.blocks.ListBlock(isi_mip.pages.blocks.SectorBlock)))))))),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('teaser_title', models.CharField(max_length=500)),
                ('teaser_text', wagtail.wagtailcore.fields.RichTextField()),
                ('teaser_link_external', models.URLField(blank=True, help_text='Will be ignored if an internal link is provided', verbose_name='External link')),
                ('content', wagtail.wagtailcore.fields.StreamField((('row', wagtail.wagtailcore.blocks.StreamBlock((('teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('bigteaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('news', wagtail.wagtailcore.blocks.StructBlock((('blog_index', isi_mip.contrib.blocks.SpecificPageChooserBlock(help_text='Select blog index page.', required=False)), ('title', wagtail.wagtailcore.blocks.CharBlock(help_text='Per default, the title of the blog index will be used.', required=False)), ('entry_count', isi_mip.contrib.blocks.IntegerBlock(help_text='How many blog entries should be displayed?', max_value=5, min_value=1, required=True))))), ('numbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.CharBlock()), ('number2', wagtail.wagtailcore.blocks.CharBlock())))), ('twitter', wagtail.wagtailcore.blocks.StructBlock((('username', wagtail.wagtailcore.blocks.CharBlock(help_text='You will find username and widget_id @ https://twitter.com/settings/widgets/', required=True)), ('widget_id', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('tweet_limit', wagtail.wagtailcore.blocks.CharBlock(max_length=2, required=True)))))))),))),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='ImpactModelsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.StreamField((('impact_models', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()), ('rows_per_page', isi_mip.contrib.blocks.IntegerBlock(default=20, min_value=1, required=True))))), ('news', wagtail.wagtailcore.blocks.StructBlock((('blog_index', isi_mip.contrib.blocks.SpecificPageChooserBlock(help_text='Select blog index page.', required=False)), ('title', wagtail.wagtailcore.blocks.CharBlock(help_text='Per default, the title of the blog index will be used.', required=False)), ('entry_count', isi_mip.contrib.blocks.IntegerBlock(help_text='How many blog entries should be displayed?', max_value=5, min_value=1, required=True))), template='blocks/flat_blog_block.html'))))),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.wagtailroutablepage.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='LinkListPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('links', wagtail.wagtailcore.fields.StreamField((('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', wagtail.wagtailcore.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False))))),))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NewsletterPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='OutcomesPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('papers', wagtail.wagtailcore.fields.StreamField((('paper', wagtail.wagtailcore.blocks.StructBlock((('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('author', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('journal', wagtail.wagtailcore.blocks.CharBlock()), ('link', wagtail.wagtailcore.blocks.URLBlock())))),))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='OutputDataPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.StreamField((('output_data', wagtail.wagtailcore.blocks.StructBlock((('description', wagtail.wagtailcore.blocks.RichTextBlock()),))),))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RegisterFormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')], max_length=16, verbose_name='field type')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.CharField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', max_length=512, verbose_name='choices')),
                ('default_value', models.CharField(blank=True, help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='pages.FormPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='teaser_link_internal',
            field=models.ForeignKey(blank=True, help_text='If set, this has precedence over the external link.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Or internal link'),
        ),
    ]
