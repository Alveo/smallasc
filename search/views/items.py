from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Models used for querying
from search.modelspackage.sessions import Session
from search.modelspackage.components import Component
from search.modelspackage.items import Item
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


@login_required
def index (request, site_id, participant_id, session_id, component_id):
    """ Lists all the items for a particular participants session and component type. """

    items = Item.filter_by_component (SparqlLocalWrapper.create_sparql (), participant_id, session_id, component_id)

    return render (request, 'browse/items/index.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'items': items})


