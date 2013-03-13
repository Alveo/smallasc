from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers       import reverse
from django.shortcuts               import render

from browse.modelspackage           import Item, Component, Participant
from search.forms                   import ParticipantSearchForm, ParticipantSearchFilterForm, ParticipantComponentSearchForm
from search.helpers                 import append_querystring_to_url


@login_required
@permission_required('auth.can_view_item_search') 
def search(request):

    search_form         = ParticipantSearchForm(request.GET)
    all_participants    = Participant.objects.filter(search_form.generate_predicates())
    participants        = user_filtered_participants(request, all_participants)

    components = []
    for participant in participants:
        components += Component.objects.filter_by_participant(participant.friendly_id())

    components_sorted   = sorted (set(components), key = lambda comp: comp.sessionId)
    component_form      = ParticipantComponentSearchForm (participants, components_sorted, request.GET)

    if component_form.is_valid():

        items = []
        for comp in components:
            if comp.identifier in component_form.cleaned_data["components_field"]:
                items += Item.objects.filter_by_component (comp.participantId, comp.sessionId, comp.componentId) 

        return render (request, 'search/results.html', { 
            'items': items, 
            'item_ids': [item.identifier for item in items] 
        })

    else:

        return render(request, 'search/components.html', { 
            'form':                     component_form, 
            'participant_count':        len(participants),
            'participant_url':          append_querystring_to_url(request, '/browse/participants'),
            'participant_filter_url':   append_querystring_to_url(request, '/search/participants')
        }) # Should use reverse urls instead of hard coded urls



def user_filtered_participants(request, all_participants):
    
    participant_form    = ParticipantSearchFilterForm(all_participants, request.GET)

    if participant_form.is_valid():

        return participant_form.return_selected_participants()

    return all_participants