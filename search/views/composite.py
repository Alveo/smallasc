from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

# Models in usr
from search.models.sites import Sites

def index (request):
	""" The composite search view returns pretty much all the standard fieldsets in a simplified
	view. This view is meant for normal users, not power users. """
	sites = Sites.objects.all ()
	return render_to_response ('composite/index.html', {'sites': sites})


def search (request):
	""" This function shows the results of a search. """
	try:
		sites = request.GET['site']
	except (KeyError):
		return render_to_response ('composite/index.html', {
                'sites': Sites.objects.all (),
                'error_message': "You didn't select any search criteria.",
            }, context_instance = RequestContext (request)
            )
	else:
		return render_to_response ('composite/results.html', {'sites': sites})
