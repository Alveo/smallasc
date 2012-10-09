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

    component = Component.get (SparqlLocalWrapper.create_sparql (), participant_id, session_id, component_id)

    if component == None:
        return Http404("Requested component not found")

    return render (request, 'browse/items/index.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'component': component})


