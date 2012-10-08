from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Models used for querying
from search.modelspackage.participants import Participant
from search.modelspackage.components import Component
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


@login_required
def index (request, site_id, participant_id, session_id):
    """ Lists all the components for a particular session. We still keep the other ids as they
    will become useful later. """
    participant = Participant.get (SparqlLocalWrapper.create_sparql (), participant_id)
    if participant is None:
    	raise Http404 ("Requested participant not found")

    components = Component.filter_by_participant (SparqlLocalWrapper.create_sparql (), participant)

    return render (request, 'browse/components/index.html', {'components': components})


