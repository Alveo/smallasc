from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers       import reverse
from django.shortcuts               import render

from baseapp.helpers                import generate_paginated_object
from browse.modelspackage.items     import ItemManager
from browse.modelspackage.components import ComponentManager
from browse.modelspackage.participants import ParticipantManager
from search.forms                   import SearchForm, ParticipantSearchForm, ComponentSearchForm
from search.forms.choice_options    import DEFAULT_SPEAKER_QUANTITY
from search.helpers                 import append_querystring_to_url


@login_required
@permission_required('auth.can_view_item_search') 
def search(request):

    participantManager = ParticipantManager(client_json=request.session.get('client',None))
    itemManager = ItemManager(client_json=request.session.get('client',None))
    search_form             = SearchForm(request.GET)
    all_participants        = participantManager.filter(search_form.generate_predicates())
    filtered_participants   = user_filtered_participants(request, all_participants)

    component_form          = create_component_search_form(request, filtered_participants)

    if component_form.is_valid():
        items = []
        for comp in component_form.return_selected_components():
            items += retrieve_items(itemManager, filtered_participants, comp, component_form.get_speaker_no()) 

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


def retrieve_items(itemManager, participants, component, speaker_limit):
    items = []
    count = 0

    for participant in participants:
        if count < speaker_limit:
            items += itemManager.filter_by_component(
                        participant.friendly_id(), 
                        component.sessionId, 
                        component.componentId
                    ) 

        count += 1

    return items


def create_component_search_form(request, participants):
    
    componentManager = ComponentManager(client_json=request.session.get('client',None))
    
    components = []
    for participant in participants:
        components +=componentManager.filter_by_participant(participant.friendly_id())

     # The use of a set ensures items are unique
    components_sorted   = sorted(set(components), key = lambda comp: comp.sessionId)

    bound_data = request.GET.copy()
    if not 'speaker_no_field' in bound_data:
        bound_data['speaker_no_field'] = DEFAULT_SPEAKER_QUANTITY

    return ComponentSearchForm(participants, components_sorted, bound_data)


def user_filtered_participants(request, all_participants):
    
    participant_form  = ParticipantSearchForm(all_participants, request.GET)
    if participant_form.is_valid():
        return participant_form.return_selected_participants()

    return all_participants