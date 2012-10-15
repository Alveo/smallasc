from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response

from search.modelspackage.sites import Site


@login_required
def index (request):
    """ The sites index view displays all the available sites current in the RDF store. """

    sites = Site.objects.all ()
    return render (request, 'browse/sites/index.html', {'sites': sites})


