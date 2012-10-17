from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Models used for querying
from search.modelspackage.sessions import Session
from search.modelspackage.components import Component
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


@login_required
def index (request, site_id, participant_id, session_id):
    """ Lists all the components for a particular session. We still keep the other ids as they
    will become useful later. """


    components = Component.objects.filter_by_session (site_id, participant_id, session_id)

    return render (request, 'browse/components/index.html', 
        {'site_id' : site_id,
         'participant_id' : participant_id,
         'session_id' : session_id,
         'components': components})


