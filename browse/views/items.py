from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# Models used for querying
from browse.modelspackage.sites import Site, SiteManager
from browse.modelspackage.sessions import Session
from browse.modelspackage.items import Item, ItemManager

from baseapp.helpers import generate_breadcrumbs

@login_required
@permission_required('auth.can_view_items')
def index (request, site_id, participant_id, session_id, component_id, template = 'browse/items/index.html'):

    siteManager = SiteManager(client_json=request.session.get('client',None))
    itemManager = ItemManager(client_json=request.session.get('client',None))

    site = siteManager.get (site_id)
    items = itemManager.filter_by_component (participant_id, session_id, component_id)
    item_ids = [ item.identifier for item in items ]

    breadcrumbs = generate_breadcrumbs(request,site)

    return render (request, template,
        {'site_id' : site_id,
         'site' : site,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'component_id': component_id,
         'items': items,
         'item_ids' : item_ids,
         'zipname' : participant_id + "-" + component_id,
         'breadcrumbs' : breadcrumbs })

@login_required
@permission_required('auth.can_view_item')
def show (request, site_id, participant_id, session_id, component_id, basename, template = 'browse/items/show.html'):

    siteManager = SiteManager(client_json=request.session.get('client',None))
    itemManager = ItemManager(client_json=request.session.get('client',None))

    site = siteManager.get (site_id)
    item = itemManager.get (participant_id, basename)

    breadcrumbs = generate_breadcrumbs(request,site)

    if item is None:
        return Http404("Item not found %s" % basename)

    return render (request, 'browse/items/show.html',
        {'site_id' : site_id,
         'site' : site,
         'participant_id' : participant_id,
         'component_id' :  component_id,
         'session_id' : session_id,
         'item': item,
         'breadcrumbs' : breadcrumbs, })
