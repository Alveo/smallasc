from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers       import reverse
from django.shortcuts               import render

from browse.modelspackage           import Item, Component, Participant
from search.forms                   import ParticipantSearchForm, ParticipantSearchFilterForm, ParticipantComponentSearchForm
from search.helpers                 import append_querystring_to_url


@login_required
@permission_required('auth.can_view_item_search') 
def search(request):

    search_form             = ParticipantSearchForm(request.GET)
    all_participants        = Participant.objects.filter(search_form.generate_predicates())
    filtered_participants   = user_filtered_participants(request, all_participants)

    components = []
    for participant in filtered_participants:
        components += Component.objects.filter_by_participant(participant.friendly_id())


    components_sorted   = sorted(set(components), key = lambda comp: comp.sessionId) # The use of set ensures items are unique
    component_form      = ParticipantComponentSearchForm(filtered_participants, components_sorted, request.GET)

    if component_form.is_valid():

        items = []

        for comp in component_form.return_selected_components():
            for participant in filtered_participants:
            
                print "Component %s with participant identifier %s" % (comp.identifier, participant.friendly_id())

                items += Item.objects.filter_by_component(participant.friendly_id(), comp.sessionId, comp.componentId) 

        return render (request, 'search/results.html', { 
            'items': items, 
            'item_ids': [item.identifier for item in items] 
        })

    else:

        return render(request, 'search/components.html', { 
            'form':                     component_form, 
            'participant_count':        len(filtered_participants),
            'participant_url':          append_querystring_to_url(request, '/browse/participants'),
            'participant_filter_url':   append_querystring_to_url(request, '/search/participants')
        }) # Should use reverse urls instead of hard coded urls



def user_filtered_participants(request, all_participants):
    
    participant_form    = ParticipantSearchFilterForm(all_participants, request.GET)

    print request.GET

    if participant_form.is_valid():

        print "User filtered participants %s" % (participant_form.return_selected_participants())

        return participant_form.return_selected_participants()


    return all_participants