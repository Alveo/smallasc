from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Local types
from search.modelspackage.sites import Site
from search.modelspackage.participants import Participant
from search.modelspackage.sessions import Session
from search.modelspackage.education_history import EducationHistory
from search.modelspackage.professional_history import ProfessionalHistory
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


@login_required
def index (request, site_id):
    """ The sites index view displays all the available sites current in the RDF store. 
        HTTP Verb /GET: Url /browse/sites/:id/participants/ """
    site = Site.get (SparqlLocalWrapper.create_sparql (), site_id)
    if site is None:
        raise Http404 ("Requested site not found")

    # If we have a site, then let's get it's participants
    participants = Participant.all ((SparqlLocalWrapper.create_sparql ()), site)
    return render (request, 'browse/participants/index.html', 
        {
            'participants': participants,
            'site': site,
            'site_id': site_id
        })


@login_required
def show (request, site_id, participant_id):
    """ This view shows the details of a particular participant. 
        HTTP Verb /GET: Url /browse/sites/:id/participants/:id """
    participant = Participant.get (SparqlLocalWrapper.create_sparql (), participant_id)
    if participant is None:
        raise Http404 ("Requested participant not found")

    site = Site.get (SparqlLocalWrapper.create_sparql (), site_id)
    if site is None:
        raise Http404 ("Requested site not found")

    sessions = Session.filter_by_participant (SparqlLocalWrapper.create_sparql (), participant)
    education_history = EducationHistory.filter_by_participant (SparqlLocalWrapper.create_sparql (), participant)
    professional_history = ProfessionalHistory.filter_by_participant (SparqlLocalWrapper.create_sparql (), participant)

    return render (request, 'browse/participants/show.html', 
        {
            'participant': participant,
            'site': site,
            'site_id': site_id,
            'sessions': sessions,
            'education_history': education_history,
            'professional_history': professional_history
        })


