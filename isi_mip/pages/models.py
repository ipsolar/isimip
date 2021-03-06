from blog.models import BlogIndexPage as _BlogIndexPage
from blog.models import BlogPage as _BlogPage
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout, password_change
from django.core.urlresolvers import reverse
from django.db import models
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.text import slugify
from modelcluster.fields import ParentalKey

from wagtail.wagtailsearch import index
from wagtail.contrib.wagtailroutablepage.models import route, RoutablePageMixin
from wagtail.wagtailadmin.edit_handlers import *
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm

from isi_mip.climatemodels.blocks import InputDataBlock, OutputDataBlock, ImpactModelsBlock
from isi_mip.climatemodels.models import BaseImpactModel
from isi_mip.climatemodels.views import (
    impact_model_details, impact_model_edit, input_data_details,
    impact_model_download, participant_download, show_participants, STEP_BASE, STEP_DETAIL, STEP_TECHNICAL_INFORMATION,
    STEP_INPUT_DATA, STEP_OTHER, STEP_SECTOR,
    duplicate_impact_model, create_new_impact_model, update_contact_information_view)
from isi_mip.contrib.blocks import BlogBlock, smart_truncate
from isi_mip.core.views import search
from isi_mip.pages.blocks import *
from isi_mip.contrib.forms import AuthenticationForm


class BlogPage(_BlogPage):
    parent_page_types = ['pages.BlogIndexPage']

    search_fields = _BlogPage.search_fields + [
        index.SearchField('body')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog'] = self
        try:
            rendition = self.header_image.get_rendition('max-800x800')
            context['image'] = {'url': rendition.url, 'name': self.header_image.title}
        except:
            pass
        return context


class BlogIndexPage(_BlogIndexPage):
    subpage_types = ['pages.BlogPage']
    description = RichTextField(null=True, blank=True)
    flat = models.BooleanField(default=False, help_text='Whether or not the index page should display items as a flat list or as blocks.')

    content_panels = _BlogIndexPage.content_panels + [
        RichTextFieldPanel('description'),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('flat'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        entries = self.blogs
        context['title'] = self.title

        context['entries'] = []
        for entry in entries:
            body = '' if entry.body.strip() == '<p><br/></p>' else entry.body
            entry_context = {
                'date': entry.date,
                'href': entry.slug,
                'description': smart_truncate(body, 300, 350),
                'title': entry.title,
                'arrow_right_link': True
            }
            try:
                rendition = entry.header_image.get_rendition('fill-640x360-c100')
                entry_context['image'] = {'url': rendition.url, 'name': entry.header_image.title}
                entry_context['description'] = smart_truncate(body, 0, 100)
            except:
                pass
            context['entries'] += [entry_context]
        return context

    def serve(self, request, *args, **kwargs):
        if self.flat:
        # if 'flat' in request.GET and request.GET['flat'] == 'True':
            self.template = 'pages/blog_index_flat_page.html'
        return super(BlogIndexPage, self).serve(request, *args, **kwargs)


class TOCPage(Page):
    show_toc = models.BooleanField(default=False, help_text='Show Table of Contents')

    settings_panels = Page.settings_panels + [
        FieldPanel('show_toc'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.show_toc:
            context['toc'] = []
            for block in self.content:
                if block.block_type == 'heading':
                    link = "#"+slugify(block.value, allow_unicode=True)
                    context['toc'] += [{'href': link, 'text': block.value}]
        return context

    class Meta:
        abstract = True


class RoutablePageWithDefault(RoutablePageMixin, TOCPage):
    @route(r'^$')
    def base(self, request):
        return TemplateResponse(
            request,
            self.get_template(request),
            self.get_context(request)
        )

    class Meta:
        abstract = True


class GenericPage(TOCPage):
    template = 'pages/default_page.html'
    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS)
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]


class HomePage(RoutablePageWithDefault):
    parent_page_types = ['wagtailcore.Page']

    teaser_title = models.CharField(max_length=500)
    teaser_text = RichTextField()
    teaser_link_external = models.URLField("External link", blank=True,
                                           help_text="Will be ignored if an internal link is provided")
    teaser_link_internal = models.ForeignKey(
        'wagtailcore.Page',
        verbose_name="Or internal link",
        help_text='If set, this has precedence over the external link.',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content = StreamField([
        ('row', RowBlock([
            ('teaser', SmallTeaserBlock()),
            ('bigteaser', BigTeaserBlock(wideimage=True)),
            ('blog', BlogBlock()),
            ('numbers', IsiNumbersBlock()),
            ('twitter', TwitterBlock()),
        ])
         )
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('teaser_title'),
            RichTextFieldPanel('teaser_text'),
            MultiFieldPanel([
                FieldPanel('teaser_link_external'),
                PageChooserPanel('teaser_link_internal'),

            ]),
        ], heading='Teaser'),
        StreamFieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('teaser_text'),
        index.SearchField('teaser_title', partial_match=True),
        index.SearchField('content'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if self.teaser_link_internal:
            link = self.teaser_link_internal.url
        else:
            link = self.teaser_link_external
        context['teaser'] = {
            'title': self.teaser_title,
            'text': self.teaser_text,
            'button': {
                'href': link,
                'text': 'Read more',
                'fontawesome': 'facebook',
            }
        }
        context['noborder'] = True
        return context

    @route(r'search/$')
    def search(self, request):
        subpage = {'title': 'Search', 'url': ''}
        context = {'page': self, 'subpage': subpage, 'headline': ''}
        return search(request, extra_context=context)


class AboutPage(TOCPage):
    template = 'pages/default_page.html'

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('pdf', PDFBlock()),
        ('paper', PaperBlock(template='widgets/page-teaser-wide.html')),
        ('bigteaser', BigTeaserBlock()),
        ('contact', ContactsBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]


class GettingStartedPage(RoutablePageWithDefault):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage, 'GettingStartedPage']

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('protocol', ProtocolBlock()),
        ('input_data', InputDataBlock()),
        ('contact', ContactsBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),

    ])
    input_data_description = RichTextField(null=True, blank=True, verbose_name='Input Data Details Description')

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
    details_content_panels = [
        RichTextFieldPanel('input_data_description'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(details_content_panels, heading='Input Data Details'),
        ObjectList(RoutablePageWithDefault.promote_panels, heading='Promote'),
        ObjectList(RoutablePageWithDefault.settings_panels, heading='Settings', classname="settings"),
    ])
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

    @route(r'^details/(?P<id>\d+)/$')
    def details(self, request, id):
        return input_data_details(self, request, id)


class ImpactModelsPage(RoutablePageWithDefault):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('impact_models', ImpactModelsBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),
    ])
    private_model_message = models.TextField()
    common_attributes_text = models.TextField()

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
    settings_panels = RoutablePageWithDefault.settings_panels + [
        FieldPanel('private_model_message'),
        FieldPanel('common_attributes_text'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

    @route(r'^details/(?P<id>\d+)/$')
    def details(self, request, id):
        return impact_model_details(self, request, id)

    @route(r'edit/(?P<id>[0-9]*)/$')
    def edit_base(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_BASE)

    @route(r'edit/model-reference/(?P<id>[0-9]*)/$')
    def edit_detail(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_DETAIL)

    @route(r'edit/resolution/(?P<id>[0-9]*)/$')
    def edit_technical_information(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_TECHNICAL_INFORMATION)

    @route(r'edit/input-data/(?P<id>[0-9]*)/$')
    def edit_input_data(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_INPUT_DATA)

    @route(r'edit/model-setup/(?P<id>[0-9]*)/$')
    def edit_other(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_OTHER)

    @route(r'edit/sector/(?P<id>[0-9]*)/$')
    def edit_sector(self, request, id=None):
        return impact_model_edit(self, request, id, STEP_SECTOR)

    @route(r'duplicate/(?P<impact_model_id>[0-9]*)/(?P<simulation_round_id>[0-9]*)/$')
    def duplicate(self, request, impact_model_id=None, simulation_round_id=None):
        return duplicate_impact_model(self, request, impact_model_id, simulation_round_id)

    @route(r'create/(?P<base_model_id>[0-9]*)/(?P<simulation_round_id>[0-9]*)/$')
    def create(self, request, base_model_id=None, simulation_round_id=None):
        return create_new_impact_model(self, request, base_model_id, simulation_round_id)

    @route(r'download/$')
    def download(self, request):
        return impact_model_download(self, request)


class OutputDataPage(TOCPage):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('output_data', OutputDataBlock()),
        ('blog', BlogBlock(template='blocks/flat_blog_block.html')),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]


class OutcomesPage(TOCPage):
    template = 'pages/default_page.html'

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('papers', PapersBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]


class FAQPage(TOCPage):
    template = 'pages/default_page.html'
    parent_page_types = [HomePage]

    content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS + [
        ('faqs', FAQsBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]


class LinkListPage(TOCPage):
    template = 'pages/default_page.html'

    content = StreamField(BASE_BLOCKS + [
        ('links', ListBlock(LinkBlock(), template='blocks/link_list_block.html', icon='fa fa-list-ul')),
        ('supporters', SupportersBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]


class DashboardPage(RoutablePageWithDefault):
    impact_models_description = RichTextField(null=True, blank=True)
    content_panels = Page.content_panels + [
        RichTextFieldPanel('impact_models_description'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        base_impact_models = request.user.userprofile.owner.all().order_by('name')
        if request.user.is_authenticated() and request.user.is_superuser:
            base_impact_models = BaseImpactModel.objects.all()
        impage = ImpactModelsPage.objects.get()
        impage_details = lambda imid: "<span class='action'><a href='{0}' class=''>{{0}}</a></span>".format(
            impage.url + impage.reverse_subpage('details', args=(imid, )))
        impage_edit = lambda imid: "<span class='action'><i class='fa fa-edit'></i> <a href='{0}' class=''>Edit model information for {{0}}</a></span>".format(
            impage.url + impage.reverse_subpage('edit_base', args=(imid,)))
        impage_create = lambda bmid, srid: "<span class='action'><i class='fa fa-file-o'></i> <a href='{0}' class=''>Enter ALL new model information for {{0}}</a></span>".format(
            impage.url + impage.reverse_subpage('create', args=(bmid, srid)))
        impage_duplicate = lambda imid, srid: "<span class='action'><i class='fa fa-files-o'></i> <a href='{0}' class=''>Use model information for {{0}} as starting point for {{1}}</a></span>".format(
            impage.url + impage.reverse_subpage('duplicate', args=(imid, srid)))
        context['head'] = {
            'cols': [{'text': 'Model'}, {'text': 'Sector'}, {'text': 'Simulation round'}, {'text': 'Public'}, {'text': 'Action'}]
        }

        bodyrows = []
        for bims in base_impact_models:
            for imodel in bims.impact_model.all():
                values = [
                    [impage_details(bims.id).format(bims.name)],
                    [bims.sector.name],
                    [imodel.simulation_round.name],
                    ['<i class="fa fa-{}" aria-hidden="true"></i>'.format('check' if imodel.public else 'times')],
                    [impage_edit(imodel.id).format(imodel.simulation_round.name)],
                ]
                row = {
                    'cols': [{'texts': x} for x in values],
                }
                bodyrows.append(row)
            duplicate_impact_model = bims.can_duplicate_from()
            for sr in bims.get_missing_simulation_rounds():
                duplicate_model_text = ''
                if duplicate_impact_model:
                    duplicate_model_text = impage_duplicate(duplicate_impact_model.id, sr.id).format(duplicate_impact_model.simulation_round, sr.name)
                values = [
                    [bims.name],
                    [bims.sector.name],
                    [sr.name],
                    [],
                    [
                        impage_create(bims.id, sr.id).format(sr.name),
                        duplicate_model_text
                    ],
                ]
                row = {
                    'cols': [{'texts': x} for x in values],
                }
                bodyrows.append(row)
        context['body'] = {'rows': bodyrows}
        if request.user.groups.filter(name='ISIMIP-Team').exists():
            context['show_participants_link'] = True
        return context

    @route(r'^$')
    def base(self, request):
        if not request.user.is_authenticated():
            messages.info(request, 'This is a restricted area. To proceed you need to log in.')
            return HttpResponseRedirect(self.reverse_subpage('login'))

        return TemplateResponse(
            request,
            self.get_template(request),
            self.get_context(request)
        )

    @route(r'participants/$')
    def participants(self, request):
        if not request.user.is_authenticated():
            messages.info(request, 'This is a restricted area. To proceed you need to log in.')
            return HttpResponseRedirect(self.reverse_subpage('login'))
        subpage = {'title': 'ISIMIP participants', 'url': ''}
        context = {'page': self, 'subpage': subpage, 'headline': ''}
        return show_participants(request, extra_context=context)

    @route(r'download/$')
    def download(self, request):
        if not request.user.is_authenticated():
            messages.info(request, 'This is a restricted area. To proceed you need to log in.')
            return HttpResponseRedirect(self.reverse_subpage('login'))
        return participant_download(self, request)

    @route(r'logout/$')
    def logout(self, request):
        subpage = {'title': 'Logout', 'url': ''}
        context = {'page': self, 'subpage': subpage, 'headline': ''}
        return logout(request, extra_context=context)

    @route(r'login/$')
    def login(self, request):
        subpage = {'title': 'Login', 'url': ''}
        context = {'page': self, 'subpage': subpage, 'headline': ''}
        return login(request, extra_context=context, authentication_form=AuthenticationForm)

    @route(r'change-password/$')
    def change_password(self, request):
        if not request.user.is_authenticated():
            messages.info(request, 'This is a restricted area. To proceed you need to log in.')
            return HttpResponseRedirect(self.reverse_subpage('login'))
        subpage = {'title': 'Change password', 'url': ''}
        context = {'page': self, 'subpage': subpage, 'headline': ''}
        return password_change(request, extra_context=context)

    @route(r'update-contact-information/$')
    def update_contact_information(self, request):
        if not request.user.is_authenticated():
            messages.info(request, 'This is a restricted area. To proceed you need to log in.')
            return HttpResponseRedirect(self.reverse_subpage('login'))
        subpage = {'title': 'Update contact information', 'url': ''}
        context = {'page': self, 'subpage': subpage, 'headline': ''}
        return update_contact_information_view(request, self, extra_context=context)


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    landing_page_template = 'pages/form_page_confirmation.html'
    subpage_types = []

    top_content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS)
    confirmation_text = models.TextField(default='Your registration was submitted')
    bottom_content = StreamField(BASE_BLOCKS + COLUMNS_BLOCKS)

    button_name = models.CharField(max_length=500, verbose_name='Button name', default='Submit')

    content_panels = AbstractEmailForm.content_panels + [
        StreamFieldPanel('top_content'),
        StreamFieldPanel('bottom_content')
    ]
    form_content_panels = [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('button_name'),
        FieldPanel('confirmation_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('to_address', classname="full"),
            FieldPanel('from_address', classname="full"),
            FieldPanel('subject', classname="full"),
        ], "Email"),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('top_content'),
        index.SearchField('bottom_content'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(form_content_panels, heading='Form Builder'),
        ObjectList(AbstractEmailForm.promote_panels, heading='Promote'),
        ObjectList(AbstractEmailForm.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        message = {'tags': 'success', 'text': self.confirmation_text}
        context['confirmation_messages'] = [message]
        return context
