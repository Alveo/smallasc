from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# Local types
from browse.modelspackage.sites import Site
from browse.modelspackage.participants import Participant
from browse.modelspackage.sessions import Session
from browse.modelspackage.residence_history import ResidenceHistory 
from browse.modelspackage.language_usage import LanguageUsage
from search.forms import ParticipantSearchForm


@login_required
@permission_required('auth.can_view_participants')
def index(request, site_id):

    site = Site.objects.get(site_id)
    if site is None:
        search_form = ParticipantSearchForm (request.GET)
        participants = Participant.objects.filter (search_form.generate_predicates())
    else:
        participants = Participant.objects.with_data(site)
    
    part_ids = [ part.identifier for part in participants ]
    return render (request, 'browse/participants/index.html', {
        'participants': participants,
        'site': site,
        'site_id': site_id,
        'item_ids' : part_ids,
    })


@login_required
@permission_required('auth.can_view_participant')
def show (request, site_id, participant_id):
        
    participant = Participant.objects.get (participant_id)
    if participant is None:
        raise Http404 ("Requested participant not found")

    site = Site.objects.get (site_id)
    if site is None:
        raise Http404 ("Requested site not found")

    sessions = Session.objects.filter_by_participant (participant) 
    rhist = ResidenceHistory.objects.filter_by_participant(participant)
    lang = LanguageUsage.objects.filter_by_participant(participant)
    
    return render (request, 'browse/participants/show.html', 
        {
            'participant': participant,
            'site': site,
            'site_id': site_id, 
            'sessions': sessions,
            'residential_history': rhist,
            'language_usage': lang,
            'item_ids' : [ participant.identifier ],
        })


