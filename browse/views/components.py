from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# Models used for querying
from browse.modelspackage.sites import Site,SiteManager
from browse.modelspackage.components import Component, ComponentManager

from baseapp.helpers import generate_breadcrumbs

@login_required
@permission_required('auth.can_view_components')
def index (request, site_id, participant_id, session_id, template = 'browse/components/index.html'):

    siteManager = SiteManager(client_json=request.session.get('client',None))

    site = siteManager.get (site_id)
    
    componentManager = ComponentManager(client_json=request.session.get('client',None))
    
    components = componentManager.filter_by_session (site_id, participant_id, session_id)
    component_ids = [ component.identifier for component in components ]

    breadcrumbs = generate_breadcrumbs(request,site)

    return render (request, template, 
        {'site_id' : site_id,
         'site': site,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'components': components,
         'item_ids' : component_ids,
         'breadcrumbs' : breadcrumbs })


