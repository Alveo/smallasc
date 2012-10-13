from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager


class SessionManager (SparqlManager):
    """ A session is a logical representation of the actual recording session
    which takes place at a particular location."""


    def all (self):
        """ Returns all the session names """
        sparql_results = self.query ("""
            select ?rs ?session ?name 
            where {
                ?rs rdf:type austalk:RecordedSession .
                ?rs austalk:prototype ?session . 
                ?session austalk:name ?name .
            }
            ORDER BY ?name""")

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Session (
                                prototype   = result["session"]["value"],
                                identifier  = result["rs"]["value"], 
                                name        = result["name"]["value"]))

        return results


    def get (self, session_id):
        """ Returns all sessions with this session id """
        
        sparql_results = self.query ("""
            select ?rs ?session ?name 
            where {
                ?rs rdf:type austalk:RecordedSession .
                ?rs austalk:prototype ?session .
                ?rs rdfs:label  <%s> .
                ?session austalk:name ?name .
            }""" % (session_id))

        for result in sparql_results["results"]["bindings"]:
            return Session (
                        identifier  = result["rs"]["value"],
                        prototype   = result["session"]["value"], 
                        name        = result["name"]["value"])

        return None


    def filter_by_participant (self, participant):
        """ Returns all the session names for a participant """
        
        sparql_results = self.query ("""
            select ?rs ?session ?name ?number
            where {
                ?rs rdf:type austalk:RecordedSession .
                ?rs olac:speaker <%s> .
                ?rs austalk:prototype ?session .
                ?session austalk:name ?name .
                ?session austalk:id ?number .
            }
            ORDER BY ?name""" % participant.identifier)
        
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Session (
                                identifier      = result["rs"]["value"],
                                prototype       = result["session"]["value"],
                                name            = result["name"]["value"],
                                number          = result["number"]["value"]))

        return results

		
class Session (SparqlModel):

    # custom manager
    objects = SessionManager ()

    # Note that id is not specified as this is a Django model
    prototype       = models.URLField ()
    name            = models.TextField ()
    number          = models.TextField ()


    def __unicode__ (self):
        """ Simple name representation for a session """
        return self.name


    class Meta:
        app_label = 'search'