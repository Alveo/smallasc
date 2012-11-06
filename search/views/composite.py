from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Models in use
from browse.modelspackage import Item
from search.forms.composite_search import CompositeSearchForm

@login_required
def index (request):
	""" The composite search view returns pretty much all the standard fieldsets in a simplified
	view. This view is meant for normal users, not power users. """
	form = CompositeSearchForm ()
	return render (request, 'composite/index.html', {'form': form})

    

@login_required
def search (request):
    """ This function shows the results of a browse. """
    
    form = CompositeSearchForm (request.GET)
    
    if form.is_valid ():
        prompt = form.cleaned_data['prompt']
        components = form.cleaned_data['components']
        wholeword = form.cleaned_data['wholeword']
        
        result = Item.objects.filter_by_prompt(prompt, components, wholeword)
        item_ids = [ item.identifier for item in result ]
        
        #return render(request, 'composite/results.html', {'result': result})
    
        return render (request, 'composite/results.html', 
        {'site_id' : None,
         'participant_id' : None,
         'session_id' : None,
         'component_id': None,
         'items': result,
         'item_ids' : item_ids })
    
    else:
        return render(request, 'composite/index.html', {'form': form})


