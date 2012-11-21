from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Local types
#from browse.modelspackage.sites import Site, SiteManager
#from browse.modelspackage.participants import Participant, ParticipantManager
#from browse.modelspackage.sessions import Session
#from browse.modelspackage.residence_history import ResidenceHistory 
#from browse.modelspackage.language_usage import LanguageUsage
#from browse.modelspackage.sparql_local_wrapper import SparqlLocalWrapper

import surf
from browse.modelspackage.surfmodels import RecordingSite, Participant, Session


@login_required
def index (request, site_id):
    """ The sites index view displays all the available participants for this site current in the RDF store. 
        HTTP Verb /GET: Url /browse/sites/:id/participants/ """

    try:
        site = RecordingSite.objects().get_by(rdfs_label=site_id).one()
    except surf.NoResultFound:
        raise Http404 ("Requested site not found")

    # If we have a site, then let's get it's participants, just those with some data uploaded
    participants = Participant.objects().get_by_site(site)
    
    part_ids = [ part.subject for part in participants ]

    return render (request, 'browse/participants/index.html', 
        {
            'participants': participants,
            'site': site,
            'site_id': site_id,
            'item_ids' : part_ids,
        })


@login_required
def show (request, site_id, participant_id):
    """ This view shows the details of a particular participant. 
        HTTP Verb /GET: Url /browse/sites/:id/participants/:id """
        
    try:
        participant = Participant.objects().get_by(austalk_id=participant_id).one()
        participant.load()
    except surf.NoResultFound: 
        raise Http404 ("Requested participant not found")

    try:
        site = RecordingSite.objects().get_by(rdfs_label=site_id).one()
    except surf.NoResultFound:
        raise Http404 ("Requested site not found")

    sessions = Session.objects().get_by(olac_speaker=participant) 
    
    #rhist = ResidenceHistory.objects.filter_by_participant(participant)
    #lang = LanguageUsage.objects.filter_by_participant(participant)
    
    return render (request, 'browse/participants/show.html', 
        {
            'participant': participant,
            'site': site,
            'site_id': site_id, 
            'sessions': sessions,
     #       'residential_history': rhist,
      #      'language_usage': lang,
            'item_ids' : [ participant.subject ],
        })


