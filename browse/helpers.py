from collections import namedtuple
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager
from browse.modelspackage.participants      import ParticipantManager
from browse.modelspackage.sessions          import SessionManager
from browse.modelspackage.residence_history import ResidenceHistoryManager
from browse.modelspackage.language_usage    import LanguageUsageManager

# Import SPARQL modules and related information
from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings
from browse.modelspackage.sparql_local_wrapper import SparqlManager

ParticipantInfo = namedtuple('ParticipantInfo', 'participant sessions residential_history languages_spoken')


def get_participant_info(request, participant_id):
    
    participantManager = ParticipantManager(client_json=request.session.get('client',None))
    sessionManager = SessionManager(client_json=request.session.get('client',None))
    languageUsageManager = LanguageUsageManager(client_json=request.session.get('client',None))
    residenceHistoryManager = ResidenceHistoryManager(client_json=request.session.get('client',None))
    
    participant = participantManager.get(participant_id)
    if not participant is None:
        sessions = sessionManager.filter_by_participant(participant) 
        rhist = residenceHistoryManager.filter_by_participant(participant)
        lang = languageUsageManager.filter_by_participant(participant)

        return ParticipantInfo(participant = participant, 
                            sessions = sessions, 
                            residential_history = rhist, 
                            languages_spoken = lang)
    else:
        raise("no participant found")



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
        
    sparql = SparqlManager()
    
    query = """
           PREFIX iso639schema:<http://downlode.org/rdf/iso-639/schema#> 
       
       SELECT (?fln as ?First_Language)
                  WHERE {
                      ?first_language iso639schema:name ?fln
                    FILTER (?first_language = %s)
                    }
                    
        """% language_url
    
    results = sparql.query(query,skipcaononicalise=True)
    
    return results["results"]["bindings"][0]["First_Language"]["value"]
        
    
    
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
