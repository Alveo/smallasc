from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Models used for querying
from browse.modelspackage.components import Component
from participantportal.settings import *

@login_required(login_url = PP_LOGIN_URL)
def index (request, site_id, participant_id, session_id):

    components = Component.objects.filter_by_session (site_id, participant_id, session_id)
    component_ids = [ component.identifier for component in components ]

    return render (request, 'components/index.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'components': components,
         'item_ids' : component_ids }
        )


