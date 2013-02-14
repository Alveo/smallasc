from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from browse.modelspackage import Item, Participant
from search.forms import PromptSearchForm, ParticipantSearchForm, ParticipantSearchFilterForm


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
    
        return render (request, 'search/results.html', {
            'site_id' : None,
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
        predicates = {}

        # TODO: Nicer way to write this?
        if not form.cleaned_data['gender'] == 'any': predicates["foaf:gender"] = form.cleaned_data['gender']
        if not form.cleaned_data['ses'] == 'any': predicates["austalk:ses"] = form.cleaned_data['ses']
        if not form.cleaned_data['highest_qual'] == 'any': predicates["austalk:education_level"] = form.cleaned_data['highest_qual']
        if not form.cleaned_data['prof_cat'] == 'any': predicates["austalk:professional_category"] = form.cleaned_data['prof_cat']
       
        form = ParticipantSearchFilterForm (Participant.objects.filter (predicates))
        return render (request, 'search/results.html', { 'form': form })
    else:
        return render (request, 'search/index.html', { 'participant_form': form })
		
		
