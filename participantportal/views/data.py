from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from browse.helpers import *
from participantportal.settings import *
from django.http import HttpResponseRedirect


@login_required(login_url = PP_LOGIN_URL)
def index (request, template = 'data.html'):
		# if the requesting user is not a member of group 'participants' then ask for login
		# this is required when the user in research tries to access participantportal
		
		if not request.user.groups.filter(name='participants') :
			print ('inside true')
			return HttpResponseRedirect("/participantportal/login")


		participant_info = get_participant_info(request.user)

		language_url = '<' + participant_info.participant.properties()['first_language'][0] + '>'
		first_language = get_language_name(language_url)
		
		language_usage = get_language_usage(participant_info.languages_spoken)


		return render (request, template, {
    		'user_profile': request.user.userprofile,
    		'participant': participant_info.participant,
    		'sessions': participant_info.sessions,
    		'residential_history': participant_info.residential_history,
    		#'language_usage': participant_info.languages_spoken,
    		'first_language' : first_language,
    		'language_usage': language_usage,
    		'scope' : 'participantportal'
         })

