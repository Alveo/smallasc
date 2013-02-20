from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from browse.modelspackage import Component, Participant
from search.forms import ParticipantComponentSearchForm


@login_required
@permission_required('auth.can_view_item_search') 
def search (request):

    form = ParticipantComponentSearchForm (request.GET)
    predicates = {}
    
    # TODO: Nicer way to write this?
    if not form.data['gender'] == 'any': 
        predicates["foaf:gender"] = form.data['gender']
    if not form.data['ses'] == 'any': 
        predicates["austalk:ses"] = form.data['ses']
    if not form.data['highest_qual'] == 'any': 
        predicates["austalk:education_level"] = form.data['highest_qual']
    if not form.data['prof_cat'] == 'any': 
        predicates["austalk:professional_category"] = form.data['prof_cat']

    form.fields["participants_field"].choices = \
        [(part.friendly_id (), part) for part in Participant.objects.filter (predicates)]

    # Retrieve the components for each participant


    return render (request, 'search/index.html', { 'form': form })