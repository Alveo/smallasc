from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from browse.modelspackage.participants import Participant
from browse.modelspackage.sessions import Session
from browse.modelspackage.residence_history import ResidenceHistory
from browse.modelspackage.language_usage import LanguageUsage
from participantportal.settings import *

@login_required(login_url = PP_LOGIN_URL)
def index (request):
  participant = Participant.objects.get (request.user)
  if participant is None:
      raise Http404("Participant not found")

  sessions = Session.objects.filter_by_participant(participant) 
  rhist = ResidenceHistory.objects.filter_by_participant(participant)
  lang = LanguageUsage.objects.filter_by_participant(participant)

  return render (request, 'data.html', {
            'participant': participant,
            'sessions': sessions,
            'residential_history': rhist,
            'language_usage': lang,
            'item_ids' : [ participant.identifier ],
        })