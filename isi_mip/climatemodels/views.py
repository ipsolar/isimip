from datetime import datetime
from collections import OrderedDict

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import urlize, linebreaks
from django.template import Template, Context

from isi_mip.climatemodels.forms import ImpactModelStartForm, ContactPersonFormset, get_sector_form, \
    BaseImpactModelForm, ImpactModelForm, TechnicalInformationModelForm, InputDataInformationModelForm, OtherInformationModelForm
from isi_mip.climatemodels.models import ImpactModel, InputData, BaseImpactModel, SimulationRound
from isi_mip.climatemodels.tools import ImpactModelToXLSX
from isi_mip.invitation.views import InvitationView
from isi_mip.core.models import Invitation

STEP_SHOW_DETAILS = 'details'
STEP_BASE = 'edit_base'
STEP_DETAIL = 'edit_detail'
STEP_TECHNICAL_INFORMATION = 'edit_technical_information'
STEP_INPUT_DATA = 'edit_input_data'
STEP_OTHER = 'edit_other'
STEP_SECTOR = 'edit_sector'

FORM_STEPS = OrderedDict([
    (STEP_BASE, {'form': BaseImpactModelForm, 'next': STEP_DETAIL, 'verbose_name': 'Basic'}),
    (STEP_DETAIL, {'form': ImpactModelForm, 'next': STEP_TECHNICAL_INFORMATION, 'verbose_name': 'Model reference'}),
    (STEP_TECHNICAL_INFORMATION, {'form': TechnicalInformationModelForm, 'next': STEP_INPUT_DATA, 'verbose_name': 'Resolution'}),
    (STEP_INPUT_DATA, {'form': InputDataInformationModelForm, 'next': STEP_OTHER, 'verbose_name': 'Input data'}),
    (STEP_OTHER, {'form': OtherInformationModelForm, 'next': STEP_SECTOR, 'verbose_name': 'Model setup'}),
    (STEP_SECTOR, {'form': None, 'next': None, 'verbose_name': 'Sector-specific information'})
])


def impact_model_details(page, request, id):
    try:
        base_model = BaseImpactModel.objects.get(id=id)
    except:
        messages.warning(request, 'Unknown model')
        return HttpResponseRedirect('/impactmodels/')
    title = 'Impact model: %s' % base_model.name
    subpage = {'title': title, 'url': ''}
    context = {'page': page, 'subpage': subpage, 'headline': ''}
    can_edit_model = False
    if request.user in base_model.owners.all() or request.user.is_superuser:
        can_edit_model = True

    # context['editlink'] += ' | <a href="{}">admin edit</a>'.format(
    #     urlresolvers.reverse('admin:climatemodels_impactmodel_change', args=(impactmodel.id,)))

    model_simulation_rounds = []
    for im in base_model.impact_model.all():
        im_values = im.values_to_tuples() + im.fk_sector.values_to_tuples()
        model_details = []
        for k, v in im_values:
            if any((y for x, y in v)):
                res = {'term': k,
                       'definitions': ({'text': "%s: <i>%s</i>" % (x, y), 'key': x, 'value': y} for x, y in v if y)
                       }
                model_details.append(res)
        if model_details:
            model_details[0]['opened'] = True
        edit_link = ''
        if can_edit_model:
            edit_link = '<i class="fa fa-cog" aria-hidden="true"></i> <a href="{}">Edit model information for simulation round {}</a>'.format(page.url + page.reverse_subpage(STEP_BASE, args=(im.id,)), im.simulation_round.name)
        model_simulation_rounds.append({
            'simulation_round': im.simulation_round.name,
            'simulation_round_slug': im.simulation_round.slug,
            'model_name': base_model.name,
            'edit_link': edit_link,
            'details': model_details
        })
    context['description'] = urlize(base_model.short_description or '')
    context['model_simulation_rounds'] = model_simulation_rounds
    context['model_name'] = base_model.name
    bm_values = base_model.values_to_tuples()
    for k, v in bm_values:
        if any((y for x, y in v)):
            res = {'term': k,
                   'definitions': ({'text': "%s: <i>%s</i>" % (x, y), 'key': x, 'value': y} for x, y in v if y),
                   'opened': True
                   }
    context['base_model'] = [res, ]

    template = 'climatemodels/details.html'
    return render(request, template, context)


def impact_model_download(page, request):
    imodels = ImpactModel.objects.order_by('name')
    if 'sector' in request.GET:
        imodels = imodels.filter(sector=request.GET['sector'])
    if 'driver' in request.GET:
        imodels = imodels.filter(climate_data_sets__name=request.GET['driver'])
    if 'searchvalue' in request.GET:
        q = request.GET['searchvalue']
        query = Q(name__icontains=q) | Q(sector__icontains=q) | Q(climate_data_sets__name__icontains=q) \
                | Q(contactperson__name__icontains=q) | Q(contactperson__email__icontains=q)
        imodels = imodels.filter(query)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ImpactModels {:%Y-%m-%d}.xlsx"'.format(datetime.now())
    ImpactModelToXLSX(response, imodels)
    return response


def input_data_details(page, request, id):
    data = InputData.objects.get(id=id)
    template = 'pages/input_data_details_page.html'
    if data.description:
        description = urlize(linebreaks(data.description))
    else:
        description = page.input_data_description or ''
    if request.user.is_superuser:
        description += ' <a href="{}">admin edit</a>'.format(
            urlresolvers.reverse('admin:climatemodels_inputdata_change', args=(data.id,)))

    subpage = {'title': 'Input data set: %s' % data.name, 'url': ''}
    context = {'page': page,
               'subpage': subpage,
               'description': description,
               'list': [
                   {
                       'notoggle': True,
                       'opened': True,
                       'definitions': [
                           {'text': 'Data Type: %s' % data.data_type},
                           {'text': 'Simulation rounds: %s' % ', '.join((x.name for x in data.simulation_round.all()))},
                           {'text': 'Scenarios: %s' % ', '.join((x.name for x in data.scenario.all()))},
                           {'text': 'Variables: %s' % ', '.join((x.as_span() for x in data.variables.all()))},
                       ]
                   },
                   {'notoggle': True, 'opened': True, 'term': 'Caveats', 'definitions': [{'text': urlize(linebreaks(data.caveats))}]},
                   {'notoggle': True, 'opened': True, 'term': 'Download Instructions',
                    'definitions': [{'text': urlize(linebreaks(data.download_instructions))}]},
               ]
               }
    return render(request, template, context)


def crossref_proxy(request):
    try:
        url = 'http://api.crossref.org/works?rows={rows}&query={query}'
        response = requests.get(url.format(rows=5, query=request.GET['query']))
        res = response.json()
    except requests.exceptions.ConnectionError as e:
        res = {
            'unavailable': True,
            'message': 'CrossRef.org is currently unavailable. Please try again later.'
        }
    return JsonResponse(res)


def create_new_impact_model(page, request, base_model_id, simulation_round_id):
    if not request.user.is_authenticated():
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)
    base_impact_model = BaseImpactModel.objects.get(id=base_model_id)
    simulation_round = SimulationRound.objects.get(id=simulation_round_id)
    if not (request.user in base_impact_model.owners.all() or request.user.is_superuser):
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)

    # Impact model
    impact_model = ImpactModel(
        base_model=base_impact_model,
        simulation_round=simulation_round,
        public=True,
    )
    impact_model.save()
    target_url = page.url + page.reverse_subpage(STEP_BASE, args=(impact_model.id,))
    messages.success(request, 'The model has been successfully created! Please make sure to go through every step to insert the data.')
    return HttpResponseRedirect(target_url)


def duplicate_impact_model(page, request, impact_model_id, simulation_round_id):
    if not request.user.is_authenticated():
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)
    impact_model = ImpactModel.objects.get(id=impact_model_id)
    simulation_round = SimulationRound.objects.get(id=simulation_round_id)
    if not (request.user in impact_model.base_model.owners.all() or request.user.is_superuser):
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)
    duplicate = impact_model.duplicate(simulation_round)
    target_url = page.url + page.reverse_subpage(STEP_BASE, args=(duplicate.id,))
    message = 'You have chosen to duplicate your model information from {0} for {1}. Please go through each step to make sure that new fields are filled out, and to make sure the information is accurate for the model version used in {1}.'
    messages.success(request, message.format(impact_model.simulation_round.name, simulation_round.name))
    return HttpResponseRedirect(target_url)


# authentication required.. #########################################################
def impact_model_edit(page, request, id, current_step):
    if not request.user.is_authenticated():
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)
    impact_model = ImpactModel.objects.get(id=id)
    if not (request.user in impact_model.base_model.owners.all() or request.user.is_superuser):
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)
    # raise Exception(request.POST)
    next_step = FORM_STEPS[current_step]["next"]
    form = FORM_STEPS[current_step]["form"]
    subpage = {
        'title': 'Impact Model: %s (%s)' % (impact_model.base_model.name, impact_model.simulation_round.name),
        'url': page.url + page.reverse_subpage('details', args=(impact_model.base_model.id,)),
        'subpage': {'title': 'Edit %s' % FORM_STEPS[current_step]['verbose_name'], 'url': ''}
    }
    steps = [{'name': k, 'verbose_name': v['verbose_name'], 'is_active': k is current_step, 'is_next': k is next_step} for k, v in FORM_STEPS.items()]
    context = {'page': page, 'subpage': subpage, 'steps': steps}
    next_parameter = request.POST.get("next")
    # define target url depending on se next param or logical next step
    if next_parameter:
        target_url = page.url + page.reverse_subpage(next_parameter, args=(impact_model.id,))
    elif current_step == STEP_SECTOR:
        # TODO find a better solution for redirect url
        target_url = '/dashboard/'
    else:
        target_url = page.url + page.reverse_subpage(next_step, args=(impact_model.id,))
    if request.method == 'GET' and not impact_model.public:
            messages.warning(request, page.private_model_message)
    if current_step == STEP_BASE:
        return impact_model_base_edit(page, request, context, impact_model, current_step, next_step, target_url)
    elif current_step == STEP_SECTOR:
        return impact_model_sector_edit(page, request, context, impact_model, target_url)
    else:
        if current_step == STEP_DETAIL:
            instance = impact_model
        elif current_step == STEP_TECHNICAL_INFORMATION:
            instance = impact_model.technicalinformation
        elif current_step == STEP_INPUT_DATA:
            instance = impact_model.inputdatainformation
        elif current_step == STEP_OTHER:
            instance = impact_model.otherinformation
        return impact_model_detail_edit(page, request, context, form, instance, current_step, next_step, target_url)


def impact_model_detail_edit(page, request, context, form, instance, current_step, next_step, target_url):
    if request.method == 'POST':
        form = form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            message = "All data have been successfully saved."
            messages.success(request, message)
            return HttpResponseRedirect(target_url)
        else:
            messages.error(request, 'Your form has errors.')
            messages.warning(request, form.errors)
    else:
        form = form(instance=instance)
    context['form'] = form
    template = 'climatemodels/%s.html' % (current_step)
    return render(request, template, context)


def impact_model_base_edit(page, request, context, impact_model, current_step, next_step, target_url):
    base_impact_model = impact_model.base_model
    if request.method == 'POST':
        form = BaseImpactModelForm(request.POST, instance=base_impact_model)
        contactform = ContactPersonFormset(request.POST, instance=base_impact_model)
        if form.is_valid() and contactform.is_valid():
            form.save()
            contactform.save()
            message = "All data have been successfully saved."
            messages.success(request, message)
            return HttpResponseRedirect(target_url)
        else:
            messages.error(request, 'Your form has errors.')
            messages.warning(request, form.errors)
            messages.warning(request, contactform.errors)
    else:
        form = BaseImpactModelForm(instance=base_impact_model)
        contactform = ContactPersonFormset(instance=base_impact_model)
    context['form'] = form
    context['cform'] = contactform
    template = 'climatemodels/%s.html' % (current_step)
    return render(request, template, context)


def impact_model_sector_edit(page, request, context, impact_model, target_url):
    formular = get_sector_form(impact_model.base_model.sector)

    if formular is None:
        return HttpResponseRedirect(target_url)

    if request.method == 'POST':
        form = formular(request.POST, instance=impact_model.fk_sector)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! All changes to your model have been saved successfully.")
            return HttpResponseRedirect(target_url)
        else:
            messages.warning(request, form.errors)
    else:
        form = formular(instance=impact_model.fk_sector)

    context['form'] = form
    context['sector'] = impact_model.base_model.sector.name
    template = 'climatemodels/{}'.format(formular.template)
    return render(request, template, context)


def impact_model_assign(request, username=None):
    if not request.user.is_superuser:
        messages.info(request, 'You need to be logged in to perform this action.')
        nexturl = reverse('wagtailadmin_login') + "?next={}".format(request.path)
        return HttpResponseRedirect(nexturl)

    user = User.objects.get(username=username)
    base_impact_model = BaseImpactModel()

    if request.method == 'POST':
        form = ImpactModelStartForm(request.POST, instance=base_impact_model)
        if form.is_valid():
            bimodel = form.cleaned_data['model']
            send_invitation_email = form.cleaned_data.pop('send_invitation_email')
            if bimodel:
                bimodel.owners.add(user)
                bimodel.save()
                messages.success(request, "{} has been added to the list of owners for \"{}\"".format(user, bimodel))
            else:
                del (form.cleaned_data['model'])
                bimodel = BaseImpactModel.objects.create(**form.cleaned_data)
                bimodel.owners.add(user)
                bimodel.public = False
                bimodel.save()
                messages.success(request, "The new model \"{}\" has been successfully created and assigned to {}".format(bimodel, user))
            if send_invitation_email:
                send_email(request, user, bimodel)
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('admin:auth_user_list'))
        else:
            messages.warning(request, form.errors)
    else:
        form = ImpactModelStartForm(instance=base_impact_model)
    template = 'climatemodels/assign.html'
    return render(request, template, {'form': form, 'owner': user})


def send_email(request, user, bimodel):
    invite = user.invitation_set.last()
    register_link = reverse('accounts:register', kwargs={'pk': user.id, 'token': invite.token})
    context = {
        'url': request.build_absolute_uri(register_link),
        'model_name': bimodel.name,
        'sector': bimodel.sector,
        'username': user.username,
        'valid_until': invite.valid_until,
    }
    invitation = Invitation.for_site(request.site)
    template = Template(invitation.subject)
    subject = template.render(Context(context))
    # Force subject to a single line to avoid header-injection
    # issues.
    subject = ''.join(subject.splitlines())
    template = Template(invitation.body)
    message = template.render(Context(context))
    user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
