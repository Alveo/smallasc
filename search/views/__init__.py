from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from search.forms import PromptSearchForm, ParticipantSearchForm

@login_required
def index (request):
    """ The composite search view returns pretty much all the standard fieldsets in a simplified
    view. This view is meant for normal users, not power users. """
    prompt_form = PromptSearchForm ()
    part_form = ParticipantSearchForm()
    
    return render (request, 'search/index.html', {'prompt_form': prompt_form,
                                                  'participant_form': part_form})

    