from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template import RequestContext
from browse.modelspackage import Component, Participant
from search.forms import ParticipantSearchForm, ParticipantSearchFilterForm, ParticipantComponentSearchForm


@login_required
@permission_required('auth.can_view_item_search') 
def search(request):

    component_form = ParticipantComponentSearchForm(request.GET)

    print "Form statuses %s, %s" % (participant_form.is_valid(), component_form.is_valid())

    # If the component form is invalid and the participant form is
    # valid then this means we can search for the component list
    if not component_form.is_valid():
        search_form = ParticipantSearchForm(request.GET)
        predicates = search_form.generate_predicates()
        participant_form = ParticipantSearchFilterForm(Participant.objects.filter(predicates), request.GET)

        # If the participant form is valid then we have all the data we need
        # so we can render the component form
        if participant_form.is_valid():
            print participant_form.cleaned_data["participants_field"]
            return render (request, 'search/index.html', { 'form': component_form })
        else:
            print participant_form.errors
    else:
        print component_form.cleaned_data
        # components = Component.objects.filter_by_participant ("")
        return render (request, 'search/index.html', { 'form': form })