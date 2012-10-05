from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

# Local types
from search.models.sites import Sites
from search.models.participants import Participants
from search.models.sparql_local_wrapper import SparqlLocalWrapper


@login_required
def index (request, site_id):
    """ The sites index view displays all the available sites current in the RDF store. """
    site = Sites.get (SparqlLocalWrapper.create_sparql (), site_id)
    if site is None:
        raise Http404 ("Requested site not found")

    # If we have a site, then let's get it's participants
    participants = Participants.all ((SparqlLocalWrapper.create_sparql ()), site)
    return render (request, 'browse/participants/index.html', 
        {
            'participants': participants,
            'site': site
        })


