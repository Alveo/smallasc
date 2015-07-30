from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from browse.modelspackage import Item, Participant
from search.forms import PromptSearchForm, ComponentSearchForm


@login_required
@permission_required('auth.can_view_prompt_search')
def search (request):
    
    pform = PromptSearchForm(request.GET) 
    
    if pform.is_valid ():
        prompt = pform.cleaned_data['prompt'] 
        
        prompts = [p.strip() for p in prompt.split(',')]
        
        result = Item.objects.filter_by_prompts(prompts)
        item_ids = [ item.identifier for item in result ]
    
        return render (request, 'search/results.html', {
            'site_id' : None,
            'participant_id' : None,
            'session_id' : None,
            'component_id': None,
            'items': result,
            'item_ids' : item_ids,
            'zipname' : '-'.join(prompts)})
    else:
        pform = PromptSearchForm()
        return render(request, 'search/prompt.html', {'prompt_form': pform})