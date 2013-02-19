from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from browse.modelspackage import Item, Participant
from search.forms import PromptSearchForm, ParticipantSearchForm, ParticipantSearchFilterForm


@login_required
@permission_required('auth.can_view_prompt_search')
def prompt_search (request):
    
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

    form = ParticipantSearchFilterForm (request.GET)
    predicates = {}

    # TODO: Nicer way to write this?
    if not form.data['gender'] == 'any': 
        predicates["foaf:gender"] = form.data['gender']
    if not form.data['ses'] == 'any': 
        predicates["austalk:ses"] = form.data['ses']
    if not form.data['highest_qual'] == 'any': 
        predicates["austalk:education_level"] = form.data['highest_qual']
    if not form.data['prof_cat'] == 'any': 
        predicates["austalk:professional_category"] = form.data['prof_cat']

    form.fields["participants_field"].choices = \
        [(part.friendly_id (), part) for part in Participant.objects.filter (predicates)]

    return render (request, 'search/index.html', { 'init_form': form })


@login_required
@permission_required('auth.can_view_item_search') 
def item_search(request):

    form = ParticipantSearchFilterForm (request.GET)
    predicates = {}

    # TODO: Nicer way to write this?
    if not form.data['gender'] == 'any': 
        predicates["foaf:gender"] = form.data['gender']
    if not form.data['ses'] == 'any': 
        predicates["austalk:ses"] = form.data['ses']
    if not form.data['highest_qual'] == 'any': 
        predicates["austalk:education_level"] = form.data['highest_qual']
    if not form.data['prof_cat'] == 'any': 
        predicates["austalk:professional_category"] = form.data['prof_cat']

    form.fields["participants_field"].choices = \
        [(part.friendly_id (), part) for part in Participant.objects.filter (predicates)]

    return render (request, 'search/items.html', { 'init_form': form })