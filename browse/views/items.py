from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Models used for querying
from browse.modelspackage.sessions import Session
from browse.modelspackage.components import Component
from browse.modelspackage.items import Item
from browse.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


@login_required
def index (request, site_id, participant_id, session_id, component_id):
    """ Lists all the items for a particular participants session and component type. """

    items = Item.objects.filter_by_component (participant_id, session_id, component_id)

    return render (request, 'browse/items/index.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'component_id': component_id,
         'items': items})
 
@login_required
def show (request, site_id, participant_id, session_id, component_id, basename):
    """ View of an individual item. """

    item = Item.objects.get (participant_id, basename)

    if item == None:
        return Http404("Item not found %s" % basename)
    
    return render (request, 'browse/items/show.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'item': item})