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