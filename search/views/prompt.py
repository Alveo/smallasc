from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext

# Models in use
from browse.modelspackage import Item
from search.forms import PromptSearchForm, ParticipantSearchForm

@login_required
@permission_required('auth.can_view_prompt_search')
def prompt_search (request):
    """ View to show the results of a prompt search . """
    
    form = PromptSearchForm (request.GET)
    
    if form.is_valid ():
        prompt = form.cleaned_data['prompt']
        components = form.cleaned_data['components']
        wholeword = form.cleaned_data['wholeword']
        
        result = Item.objects.filter_by_prompt(prompt, components, wholeword)
        item_ids = [ item.identifier for item in result ]
    
        return render (request, 'search/results.html', 
        {'site_id' : None,
         'participant_id' : None,
         'session_id' : None,
         'component_id': None,
         'items': result,
         'item_ids' : item_ids })
    
    else:
        return render(request, 'search/index.html', {'prompt_form': form})


@login_required
@permission_required('auth.can_view_participant_search') 
def participant_search(request):

    form = ParticipantSearchForm (request.GET)
    if form.is_valid ():
      gender = form.cleaned_data['gender']
      ses = form.cleaned_data['ses']
      highest_qual = form.cleaned_data['highest_qual']
      prof_cat = form.cleaned_data['prof_cat']
      
    else:
      return render (request, 'search/index.html', {'participant_form': form})
		
		
