from django.http                            import Http404, HttpResponseRedirect
from django.contrib.auth.decorators         import login_required, permission_required
from django.shortcuts                       import render
from django.template                        import RequestContext
from django.core.urlresolvers               import reverse

from baseapp.helpers                        import generate_paginated_object
from search.forms                           import SearchForm
from browse.helpers                         import *

from browse.modelspackage.sites             import SiteManager
from browse.modelspackage.participants      import ParticipantManager
from browse.modelspackage.sessions          import SessionManager
from browse.modelspackage.residence_history import ResidenceHistoryManager
from browse.modelspackage.language_usage    import LanguageUsageManager

from baseapp.helpers import generate_breadcrumbs

@login_required
@permission_required('auth.can_view_participants')
def index(request, site_id):

    siteManager = SiteManager(client_json=request.session.get('client',None))
    participantManager = ParticipantManager(client_json=request.session.get('client',None))

    site = siteManager.get(site_id)

    if site is None:
        search_form  = SearchForm(request.GET)
        participants = participantManager.filter(search_form.generate_predicates())
    else:
        participants = participantManager.with_data(site)

    breadcrumbs = generate_breadcrumbs(request,site)

    return render(request, 'browse/participants/index.html', {
        'request'       : request,
        'site'          : site,
        'participants'  : participants,
        'breadcrumbs' : breadcrumbs
    })



@login_required
@permission_required('auth.can_view_participant')
def show_by_id(request, participant_id):
    """View of participant given just the identifier - so we can resolve
    redirects from id.austalk.edu.au"""

    participantManager = ParticipantManager(client_json=request.session.get('client',None))

    participant = participantManager.get (participant_id)

    site = participant.get_site()

    return HttpResponseRedirect(reverse('browse.views.participants.show', args=(site, participant_id)))

@login_required
@permission_required('auth.can_view_participant')
def show(request, site_id, participant_id):

    siteManager = SiteManager(client_json=request.session.get('client',None))
    participantManager = ParticipantManager(client_json=request.session.get('client',None))
    sessionManager = SessionManager(client_json=request.session.get('client',None))
    languageUsageManager = LanguageUsageManager(client_json=request.session.get('client',None))
    residenceHistoryManager = ResidenceHistoryManager(client_json=request.session.get('client',None))

    site = siteManager.get (site_id)

    if site is None:
        raise Http404 ("Requested site not found")


    participant = participantManager.get (participant_id)

    if participant is None:
        raise Http404 ("Requested participant not found")

    sessions = sessionManager.filter_by_participant (participant)
    rhist    = residenceHistoryManager.filter_by_participant(participant)
    lang     = languageUsageManager.filter_by_participant(participant)

    language_usage = get_language_usage(request, lang)

    breadcrumbs = generate_breadcrumbs(request,site)
    if 'first_language' in participant.properties().keys():
        language_url = '<' + participant.properties()['first_language'][0] + '>'
        first_language = get_language_name(request,language_url)
    else:
        first_language  = 'N/A'

    if 'father_first_language' in participant.properties().keys():
        language_url = '<' + participant.properties()['father_first_language'][0] + '>'
        father_first_language = get_language_name(request, language_url)
    else:
        father_first_language  = 'N/A'

    if 'mother_first_language' in participant.properties().keys():
        language_url = '<' + participant.properties()['mother_first_language'][0] + '>'
        mother_first_language = get_language_name(request, language_url)
    else:
        mother_first_language  = 'N/A'




    return render (request, 'browse/participants/show.html', {
        'participant':          participant,
        'site':                 site,
        'site_id':              site_id,
        'sessions':             sessions,
        'residential_history':  rhist,
        'language_usage':       language_usage,
        'item_ids' :            [ participant.identifier ],
        'breadcrumbs' : breadcrumbs,
        'first_language': first_language,
        'father_first_language': father_first_language,
        'mother_first_language': mother_first_language,
        'scope' : 'browse'

    })
