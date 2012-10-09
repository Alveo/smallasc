from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Session (models.Model):
    """ A session is a logical representation of the actual recording session
    which takes place at a particular location."""
    
    # Note that id is not specified as this is a Django model
    identifier      = models.URLField ()
    prototype       = models.URLField ()
    name            = models.TextField ()
    number          = models.TextField ()


    @staticmethod
    def all (sparql):
        """ Returns all the session names """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select distinct ?rs ?session  ?name 
            where {
                ?rs rdf:type austalk:RecordedSession .
                ?rs austalk:prototype ?session . 
                ?session austalk:name ?name .
            }
            ORDER BY ?name"""))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Session (
                                prototype   = result["session"]["value"],
                                identifier  = result["rs"]["value"], 
                                name        = result["name"]["value"]))

        return results


    @staticmethod
    def get (sparql, participant_id, session_id):
        """ Returns all sessions for this participant with this session id """
        
        qq = """
            select distinct ?rs ?session ?name 
            where {
                ?rs rdf:type austalk:RecordedSession .
                ?rs olac:speaker <http://id.austalk.edu.au/participant/%s> .
                ?rs austalk:prototype ?session .
                ?session austalk:id  %s .
                ?session austalk:name ?name .
            }""" % (participant_id, session_id)
            
        print qq
        
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query (qq))

        sparql_results = sparql.query ().convert ()

        for result in sparql_results["results"]["bindings"]:
            return Session (
                        identifier  = result["rs"]["value"],
                        prototype   = result["session"]["value"], 
                        name        = result["name"]["value"])

        return None


    @staticmethod
    def filter_by_participant (sparql, participant):
        """ Returns all the session names for a participant """
        
        qq = """
            select ?rs ?session ?id ?name ?number
            where {
                ?rs rdf:type austalk:RecordedSession .
                ?rs olac:speaker <%s> .
                ?rs austalk:prototype ?session .
                ?session austalk:name ?name .
                ?session austalk:id ?number .
            }
            ORDER BY ?name""" % participant.identifier
        
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query (qq))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Session (
                                identifier      = result["rs"]["value"],
                                prototype       = result["session"]["value"],
                                name            = result["name"]["value"],
                                number          = result["number"]["value"]))

        return results

		

    def __unicode__ (self):
        """ Simple name representation for a session """
        return self.name


    class Meta:
        app_label = 'search'