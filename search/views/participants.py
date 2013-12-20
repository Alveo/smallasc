from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers       import reverse
from django.shortcuts               import render, redirect

from browse.modelspackage           import Participant
from search.forms                   import SearchForm, ParticipantSearchForm
from search.helpers                 import append_querystring_to_url


@login_required
@permission_required('auth.can_view_participant_search') 
def search(request):

    search_form       = SearchForm(request.GET)
    participant_count = 0
    
    print "We're searching..."
    
    if search_form.is_valid():
        
        participants      = Participant.objects.filter(search_form.generate_predicates())
        participant_count = len(participants)

    	return render(request, 'search/participants.html', { 
    		'form': search_form, 
    		'participant_count': participant_count,
            'participants': participants,
    	})

    else:
        
    	return render(request, 'search/index.html', { 
            'form': search_form 
        })


@login_required
@permission_required('auth.can_view_participant_search') 
def filter(request):

    form       		  = SearchForm(request.GET)
    participant_count = 0

    if form.is_valid():
        
        participants      = Participant.objects.filter(form.generate_predicates())
        participant_count = len(participants)

        if participant_count > 0:

        	form = ParticipantSearchForm(participants, request.GET)
    		return render(request, 'search/participants.html', { 'form': form, 'participant_count': participant_count })

   	
    return render(request, 'search/index.html', { 'form': form })