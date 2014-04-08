from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# Models used for querying
from browse.modelspackage.sites import Site
from browse.modelspackage.sessions import Session
from browse.modelspackage.items import Item


@login_required
@permission_required('auth.can_view_items')
def index (request, site_id, participant_id, session_id, component_id, template = 'browse/items/index.html'):

    site = Site.objects.get (site_id)
    items = Item.objects.filter_by_component (participant_id, session_id, component_id)
    item_ids = [ item.identifier for item in items ]

    return render (request, template, 
        {'site_id' : site_id,
         'site' : site,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'component_id': component_id,
         'items': items,
         'item_ids' : item_ids,
         'zipname' : participant_id + "-" + component_id })
 
@login_required
@permission_required('auth.can_view_item')
def show (request, site_id, participant_id, session_id, component_id, basename, template = 'browse/items/show.html'):

    site = Site.objects.get (site_id)
    item = Item.objects.get (participant_id, basename)
    if item is None:
        return Http404("Item not found %s" % basename)
    
    return render (request, 'browse/items/show.html', 
        {'site_id' : site_id,
         'site' : site,
         'participant_id' : participant_id,
         'component_id' :  component_id,
         'session_id' : session_id,
         'item': item,})
