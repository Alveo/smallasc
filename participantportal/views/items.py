from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from browse.modelspackage.items import Item
from participantportal.settings import *


@login_required(login_url = PP_LOGIN_URL)
def index (request, site_id, participant_id, session_id, component_id):
    items = Item.objects.filter_by_component (participant_id, session_id, component_id)
    item_ids = [ item.identifier for item in items ]

    return render (request, 'items/index.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'component_id': component_id,
         'items': items,
         'item_ids' : item_ids })


@login_required(login_url = PP_LOGIN_URL)
def show (request, site_id, participant_id, session_id, component_id, basename):
    item = Item.objects.get (participant_id, basename)
    
    return render (request, 'items/show.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'item': item,
         'item_ids' : item.properties()['media'] })
