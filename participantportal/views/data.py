from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from browse.helpers import *
from participantportal.settings import *
from django.http import HttpResponseRedirect

@login_required(login_url = PP_LOGIN_URL)
def index (request, template = 'data.html'):
	
		if request.user.is_staff == True or request.user.is_superuser == True:
			print ('inside true')
			return HttpResponseRedirect("/participantportal/login")

		participant_info = get_participant_info(request.user)
		return render (request, template, {
		'user_profile': request.user.userprofile,
		'participant': participant_info.participant,
		'sessions': participant_info.sessions,
		'residential_history': participant_info.residential_history,
		'language_usage': participant_info.languages_spoken})