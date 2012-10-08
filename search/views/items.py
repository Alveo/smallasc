from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Models used for querying
from search.modelspackage.sessions import Session
from search.modelspackage.components import Component
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


@login_required
def index (request, site_id, participant_id, session_id, component_id):
    """ Lists all the items for a particular participants session and component type. """
    session = Session.get (SparqlLocalWrapper.create_sparql (), session_id)
    if session is None:
        raise Http404 ("Requested session not found")

    components = Component.filter_by_session (SparqlLocalWrapper.create_sparql (), session)

    return render (request, 'browse/components/index.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'components': components})


