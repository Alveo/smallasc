from collections import namedtuple
from browse.modelspackage.participants import Participant
from browse.modelspackage.sessions import Session
from browse.modelspackage.residence_history import ResidenceHistory
from browse.modelspackage.language_usage import LanguageUsage

# Import SPARQL modules and related information
from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings

ParticipantInfo = namedtuple('ParticipantInfo', 'participant sessions residential_history languages_spoken')


def get_participant_info(participant_id):
	participant = Participant.objects.get(participant_id)
	if not participant is None:
		sessions = Session.objects.filter_by_participant(participant) 
		rhist = ResidenceHistory.objects.filter_by_participant(participant)
		lang = LanguageUsage.objects.filter_by_participant(participant)

		return ParticipantInfo(participant = participant, 
                        	sessions = sessions, 
                        	residential_history = rhist, 
                        	languages_spoken = lang)



def get_language_name(language_url=''):
	"""
	Map the language name
	<http://downlode.org/rdf/iso-639/languages#en> => 'English'
	"""
	#language_url = '<http://downlode.org/rdf/iso-639/languages#en>'
	
	# Some urls may be invalid
	# For eg: participant 3_377 has "Elglish" already in mother_first_language. 
	# So dont make a SPARQL query and just return the same
	
	if "http" not in language_url:
		return language_url.replace("<", "").replace(">", "")

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
	
def get_language_usage(languages_spoken):
	# Construct a language_usage dictionary instead of participant_info.languages_spoken
	# in order to get the actual language names 
	# Eg: <http://downlode.org/rdf/iso-639/languages#en> => 'English'
	language_usage = {}
	i = 0
	for use in languages_spoken:
		language_url = '<' + use.name + '>'
		print language_url
		i = i + 1
		language_usage['lang' + str(i)] = { 'name' : get_language_name(language_url),
											'situation' : use.situation,
											'frequency' : use.frequency

											}
	return language_usage
