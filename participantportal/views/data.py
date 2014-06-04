from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from browse.helpers import *
from participantportal.settings import *
from django.http import HttpResponseRedirect

# Import SPARQL modules and related information
from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings


@login_required(login_url = PP_LOGIN_URL)
def index (request, template = 'data.html'):
		# if the requesting user is not a member of group 'participants' then ask for login
		# this is required when the user in research tries to access participantportal
		
		if not request.user.groups.filter(name='participants') :
			print ('inside true')
			return HttpResponseRedirect("/participantportal/login")


		participant_info = get_participant_info(request.user)
		webvideo_name = request.user.username + '_1_3_001-camera-0-right.mp4'

		
		

		language_url = '<' + participant_info.participant.properties()['first_language'][0] + '>'
		first_language = get_language_name(language_url)
		
		# Construct a language_usage dictionary instead of participant_info.languages_spoken
		# in order to get the actual language names 
		# Eg: <http://downlode.org/rdf/iso-639/languages#en> => 'English'
		language_usage = {}
		i = 0
		for use in participant_info.languages_spoken:
			language_url = '<' + use.name + '>'
			print language_url
			i = i + 1
			language_usage['lang' + str(i)] = { 'name' : get_language_name(language_url),
												'situation' : use.situation,
												'frequency' : use.frequency

												}
		

		return render (request, template, {
		'user_profile': request.user.userprofile,
		'participant': participant_info.participant,
		'sessions': participant_info.sessions,
		'residential_history': participant_info.residential_history,
		#'language_usage': participant_info.languages_spoken,
		'first_language' : first_language,
		'language_usage': language_usage,
		'webvideo_name': webvideo_name  })


def get_language_name(language_url=''):
	"""
	Map the language name
	<http://downlode.org/rdf/iso-639/languages#en> => 'English'
	"""
	#language_url = '<http://downlode.org/rdf/iso-639/languages#en>'
	sparql = SPARQLWrapper (settings.SPARQL_ENDPOINT)
		
	sparql.setQuery ("""
	   	PREFIX iso639schema:<http://downlode.org/rdf/iso-639/schema#> 
	   
	   SELECT (?fln as ?First_Language)
  				WHERE {
  					?first_language iso639schema:name ?fln
					FILTER (?first_language = %s)
					}
					
		"""% language_url) 

	sparql.setReturnFormat (JSON)
	results = sparql.query ().convert ()
	
	#for result in sparql_results["results"]["bindings"]:
	#print "SPARQL RESULT : ", results
	
	return results["results"]["bindings"][0]["First_Language"]["value"]
		
		
	#print 'participant: ', participant_info.languages_spoken
	
