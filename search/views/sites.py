from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from search.models.sites import Sites
from search.models.sparql_local_wrapper import SparqlLocalWrapper

@login_required
def index (request):
    """ The sites index view displays all the available sites current in the RDF store. """
    sites = Sites.all (SparqlLocalWrapper.create_sparql ())
    return render (request, 'browse/sites/index.html', {'sites': sites})


