from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers       import reverse
from django.shortcuts               import render

from baseapp.helpers                import generate_paginated_object
from browse.modelspackage           import Item, Component, Participant
from search.forms                   import SearchForm, ParticipantSearchForm, ComponentSearchForm
from search.helpers                 import append_querystring_to_url


@login_required
@permission_required('auth.can_view_item_search') 
def search(request):

    search_form             = SearchForm(request.GET)
    all_participants        = Participant.objects.filter(search_form.generate_predicates())
    filtered_participants   = user_filtered_participants(request, all_participants)

    components = []
    for participant in filtered_participants:
        components += Component.objects.filter_by_participant(participant.friendly_id())

     # The use of a set ensures items are unique
    components_sorted   = sorted(set(components), key = lambda comp: comp.sessionId)
    component_form      = ComponentSearchForm(filtered_participants, components_sorted, request.GET)

    if component_form.is_valid():
        items = []

        for comp in component_form.return_selected_components():
            for participant in filtered_participants:
                items += Item.objects.filter_by_component(participant.friendly_id(), comp.sessionId, comp.componentId) 

        return render (request, 'search/results.html', { 
            'request'   : request,
            'items'     : generate_paginated_object(request, items), 
            'item_ids'  : [item.identifier for item in items] 
        })
    else:
        return render(request, 'search/components.html', { 
            'form':                     component_form, 
            'participant_count':        len(filtered_participants),
            'participant_url':          append_querystring_to_url(request, '/browse/participants'),
            'participant_filter_url':   append_querystring_to_url(request, '/search/participants')
        }) # TODO: Should use reverse urls instead of hard coded urls


def user_filtered_participants(request, all_participants):
    
    participant_form  = ParticipantSearchForm(all_participants, request.GET)
    if participant_form.is_valid():
        return participant_form.return_selected_participants()

    return all_participants