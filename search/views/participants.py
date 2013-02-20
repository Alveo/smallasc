from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from browse.modelspackage import Item, Participant
from search.forms import PromptSearchForm, ParticipantSearchForm, ParticipantSearchFilterForm

@login_required
@permission_required('auth.can_view_participant_search') 
def search (request):

    search_form = ParticipantSearchForm(request.GET)
    if search_form.is_valid():
        predicates = search_form.generate_predicates()
        participants = Participant.objects.filter(predicates)
        participant_form = ParticipantSearchFilterForm(participants, request.GET)
        print participants
        #form.fields["participants_field"].choices = \
        #[(part.friendly_id (), part) for part in Participant.objects.filter (predicates)]
        return render (request, 'search/index.html', { 'form': participant_form })
    else:
        return render (request, 'search/index.html', { 'form': search_form })