from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template import RequestContext
from operator import attrgetter
from browse.modelspackage import Component, Participant
from search.forms import ParticipantSearchForm, ParticipantSearchFilterForm, ParticipantComponentSearchForm


@login_required
@permission_required('auth.can_view_item_search') 
def search(request):

    search_form = ParticipantSearchForm(request.GET)
    participants = Participant.objects.filter(search_form.generate_predicates())
    participant_form = ParticipantSearchFilterForm(participants, request.GET)

    # If the participant form is valid then we have all the data we need
    # so we can render the component form
    if participant_form.is_valid():
        components = []
        for part in participant_form.cleaned_data["participants_field"]:
            components = components + Component.objects.filter_by_participant(part)

        component_form = ParticipantComponentSearchForm(participants, \
            sorted(set(components), key = lambda comp: comp.sessionId), request.GET)

        if component_form.is_valid():
            print "Components %s" % (component_form.cleaned_data["components_field"])
            print "Can perform download now"

        return render (request, 'search/index.html', { 'form': component_form })
    else:
        # We should not reach this and if so render a 500 for the moment
        return HttpResponse(status=500)
