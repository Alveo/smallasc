from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager


class SessionManager (SparqlManager):
    """ A session is a logical representation of the actual recording session
    which takes place at a particular location."""


    def all (self):
        """ Returns all the session names """
        sparql_results = self.query ("""
            select distinct ?rs ?session ?name ?number ?pid ?sitename
            where {
            
                ?rs rdf:type austalk:RecordedSession .
                ?rs olac:speaker ?participant .
                
                ?participant austalk:id ?pid .
                ?participant austalk:recording_site ?site .
                ?site rdfs:label ?sitename .
                
                ?rs austalk:prototype ?session .
                ?session austalk:name ?name .
                ?session austalk:id ?number .
            }
            ORDER BY ?name""")

        results = []

        for result in sparql_results["results"]["bindings"]:

            results.append (Session (
                                identifier      = result["rs"]["value"],
                                prototype       = result["session"]["value"],
                                name            = result["name"]["value"],
                                number          = result["number"]["value"],
                                site            = result["sitename"]["value"],
                                participantId   = result["pid"]["value"]))

        return results


    def filter_by_participant (self, participant):
        """ Returns all the session names for a participant """
        
        sparql_results = self.query ("""
            select distinct ?rs ?session ?name ?number ?pid ?sitename
            where {
                BIND (<%s> AS ?participant)
            
                ?rs rdf:type austalk:RecordedSession .
                ?rs olac:speaker ?participant .
                
                ?participant austalk:id ?pid .
                ?participant austalk:recording_site ?site .
                ?site rdfs:label ?sitename .
                
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
                                number          = result["number"]["value"],
                                site            = result["sitename"]["value"],
                                participantId   = result["pid"]["value"]))

        return results

		
class Session (SparqlModel):

    # custom manager
    objects = SessionManager ()

    # Note that id is not specified as this is a Django model
    prototype       = models.URLField ()
    name            = models.TextField ()
    number          = models.TextField ()
    site            = models.TextField ()
    participantId   = models.TextField ()


    def __unicode__ (self):
        """ Simple name representation for a session """
        return self.name


    def get_absolute_url(self):
        
        return "/browse/%s/%s/%s/" % (self.site, self.participantId, self.number)

    class Meta:
        app_label = 'search'