from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response
from browse.modelspackage import Participant
from search.forms import ParticipantSearchForm, ParticipantSearchFilterForm

@login_required
@permission_required('auth.can_view_participant_search') 
def search (request):

    search_form = ParticipantSearchForm(request.GET)
    
    if search_form.is_valid():
        participants = Participant.objects.filter(search_form.generate_predicates())
        participant_form = ParticipantSearchFilterForm(participants, request.GET)
        return render (request, 'search/index.html', { 'form': participant_form })
    else:
        return render (request, 'search/index.html', { 'form': search_form })