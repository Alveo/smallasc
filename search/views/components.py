from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template import RequestContext
from operator import attrgetter
from browse.modelspackage import Item, Component, Participant
from search.forms import ParticipantSearchForm, ParticipantSearchFilterForm, ParticipantComponentSearchForm


@login_required
@permission_required('auth.can_view_item_search') 
def search (request):

    search_form = ParticipantSearchForm (request.GET)
    participants = Participant.objects.filter (search_form.generate_predicates())
    participant_form = ParticipantSearchFilterForm (participants, request.GET)

    # If the participant form is valid then we have all the data we need
    # so we can render the component form
    if participant_form.is_valid ():
        components = []
        for part in participant_form.return_selected_participants():
            components += Component.objects.filter_by_participant(part)

        component_form = ParticipantComponentSearchForm (
            participants,
            sorted (set(components), key = lambda comp: comp.sessionId),
            request.GET)

        if component_form.is_valid ():
            items = []
            for comp in components:
                if comp.identifier in component_form.cleaned_data["components_field"]:
                    items += Item.objects.filter_by_component (comp.participantId, comp.sessionId, comp.componentId) 

            item_ids = [item.identifier for item in items]
            return render (request, 'search/results.html', { 'items': items, 'item_ids': item_ids })
        else:
            return render(request, 'search/index.html', { 'form': component_form })
    else:
        # If we reach here then the user has adjusted the initial search criteria and the
        # participant form is no longer valid so we need to re-render it
        return render(request, 'search/index.html', {'form': participant_form})
