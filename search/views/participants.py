from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers       import reverse
from django.shortcuts               import render, redirect

from browse.modelspackage           import Participant
from search.forms                   import ParticipantSearchForm, ParticipantSearchFilterForm
from search.helpers                 import append_querystring_to_url


@login_required
@permission_required('auth.can_view_participant_search') 
def search(request):

    search_form       = ParticipantSearchForm(request.GET)
    participant_count = 0

    if search_form.is_valid():
        
        participants      = Participant.objects.filter(search_form.generate_predicates())
        participant_count = len(participants)

        if participant_count > 0:

            redirect_url = append_querystring_to_url(request, reverse('search.views.components.search'))
            return redirect(redirect_url)


    	return render(request, 'search/index.html', { 
    		'form': search_form, 
    		'participant_count': participant_count 
    	})

    else:

    	return render(request, 'search/index.html', { 'form': search_form })


@login_required
@permission_required('auth.can_view_participant_search') 
def filter(request):

    form       		  = ParticipantSearchForm(request.GET)
    participant_count = 0

    if form.is_valid():
        
        participants      = Participant.objects.filter(form.generate_predicates())
        participant_count = len(participants)

        if participant_count > 0:

        	form = ParticipantSearchFilterForm(participants, request.GET)
    		return render(request, 'search/participants.html', { 'form': form, 'participant_count': participant_count })

   	
    return render(request, 'search/index.html', { 'form': form })