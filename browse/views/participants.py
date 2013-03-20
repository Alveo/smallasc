from django.http                            import Http404
from django.contrib.auth.decorators         import login_required, permission_required
from django.shortcuts                       import render
from django.template                        import RequestContext

from baseapp.helpers                        import generate_paginated_object
from browse.modelspackage                   import Site, Participant, Session, ResidenceHistory, LanguageUsage
from search.forms                           import ParticipantSearchForm


@login_required
@permission_required('auth.can_view_participants')
def index(request, site_id):

    site = Site.objects.get(site_id)

    if site is None:
        search_form  = ParticipantSearchForm(request.GET)
        participants = Participant.objects.filter(search_form.generate_predicates())
    else:
        participants = Participant.objects.with_data(site)
    
    return render(request, 'browse/participants/index.html', {
        'request'       : request,
        'participants'  : generate_paginated_object(request, participants)
    })


@login_required
@permission_required('auth.can_view_participant')
def show(request, site_id, participant_id):
        
    site = Site.objects.get (site_id)

    if site is None:
        raise Http404 ("Requested site not found")


    participant = Participant.objects.get (participant_id)

    if participant is None:
        raise Http404 ("Requested participant not found")

    sessions = Session.objects.filter_by_participant (participant) 
    rhist    = ResidenceHistory.objects.filter_by_participant(participant)
    lang     = LanguageUsage.objects.filter_by_participant(participant)

    return render (request, 'browse/participants/show.html', {
        'participant':          participant,
        'site':                 site,
        'site_id':              site_id, 
        'sessions':             sessions,
        'residential_history':  rhist,
        'language_usage':       lang,
        'item_ids' :            [ participant.identifier ],
    })


