from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

from search.modelspackage.sites import Site
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


@login_required
def index (request):
    """ The sites index view displays all the available sites current in the RDF store. """
    site_model = Site ()
    sites = site_model.all ()
    return render (request, 'browse/sites/index.html', {'sites': sites})


