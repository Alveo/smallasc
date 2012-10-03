from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Models in use
from search.forms.composite_search import CompositeSearchForm

def index (request):
	""" The composite search view returns pretty much all the standard fieldsets in a simplified
	view. This view is meant for normal users, not power users. """
	form = CompositeSearchForm ()
	return render (request, 'composite/index.html', {'form': form})

def search (request):
	""" This function shows the results of a search. """
	form = CompositeSearchForm (request.GET)
	if form.is_valid ():
		return render_to_response ('composite/results.html', {
                'sites': form.cleaned_data['sites_field'],
                'sessions': form.cleaned_data['sessions_field']
            })


