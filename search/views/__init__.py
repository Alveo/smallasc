from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from search.forms import PromptSearchForm, ParticipantSearchForm

@login_required
@permission_required('auth.can_view_search') 
def index (request):
    """ The composite search view returns pretty much all the standard fieldsets in a simplified
    view. This view is meant for normal users, not power users. """
    prompt_form = PromptSearchForm ()
    part_form = ParticipantSearchForm()
    
    return render (request, 'search/index.html', {'prompt_form': prompt_form, 'init_form': part_form})

    