from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template import RequestContext
from operator import attrgetter
from browse.modelspackage import Item, Component, Participant
from search.forms import ParticipantSearchForm, ParticipantSearchFilterForm, ParticipantComponentSearchForm


@login_required
@permission_required('auth.can_view_item_search') 
def search (request):

    search_form         = ParticipantSearchForm (request.GET)
    participants        = Participant.objects.filter (search_form.generate_predicates())
    participant_form    = ParticipantSearchFilterForm (participants, request.GET)

    if participant_form.is_valid():

        components = []
        for selected_participant in participant_form.return_selected_participants():
            components += Component.objects.filter_by_participant(selected_participant)

        components_sorted = sorted (set(components), key = lambda comp: comp.sessionId)
        component_form = ParticipantComponentSearchForm (participants, components_sorted, request.GET)

        if component_form.is_valid():

            items = []
            for comp in components:
                if comp.identifier in component_form.cleaned_data["components_field"]:
                    items += Item.objects.filter_by_component (comp.participantId, comp.sessionId, comp.componentId) 

            return render (request, 'search/results.html', { 'items': items, 'item_ids': [item.identifier for item in items] })

        else:

            return render(request, 'search/index.html', { 'form': component_form })
    else:

        return render(request, 'search/index.html', {'form': participant_form})
