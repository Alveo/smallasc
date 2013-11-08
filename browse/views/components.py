from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

# Models used for querying
from browse.modelspackage.sites import Site
from browse.modelspackage.components import Component


@login_required
@permission_required('auth.can_view_components')
def index (request, site_id, participant_id, session_id, template = 'browse/components/index.html'):

    site = Site.objects.get (site_id)
    components = Component.objects.filter_by_session (site_id, participant_id, session_id)
    component_ids = [ component.identifier for component in components ]

    return render (request, template, 
        {'site_id' : site_id,
         'site': site,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'components': components,
         'item_ids' : component_ids })


