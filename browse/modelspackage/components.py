from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager


class ComponentManager (SparqlManager):

    def filter_by_session (self, site_id, participant_id, session_id):
        """ Method returns all the components filtered by the given ids. """

        sparql_results = self.query ("""
            select ?rc ?sitelabel where {

                ?participant austalk:id "%s".
                ?participant austalk:recording_site ?site .
                ?site rdfs:label ?sitelabel .
                ?rc rdf:type austalk:RecordedComponent .
                ?rc olac:speaker ?participant .
                
                ?rc dc:isPartOf ?rs .
                ?rs austalk:prototype ?ss .
                ?ss austalk:id %s .
                
        }""" % (participant_id, session_id))
        
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                        identifier      = result["rc"]["value"], 
                                        site            = result["sitelabel"]["value"],
                                        sessionId       = session_id,
                                        participantId   = participant_id,
                                      )
                            )

        return results


  

class Component (SparqlModel):
    """ A component is a logical representation of a component which belongs
    to a session."""

    # custom manager
    objects = ComponentManager ()

    site = models.TextField ()
    participantId = models.TextField ()
    shortname = models.TextField()
    sessionId = models.TextField()

    def __unicode__ (self):
        """ Simple name representation for a components """
        return self.identifier

    def get_absolute_url(self):
        """Return a canonical URL for this item"""
        p = self.prototype()             
        return "/browse/%s/%s/%s/%s/" % (self.site, self.participantId, self.sessionId, p['shortname'])    

    def session_and_comp_name(self):
        p = self.prototype()
        return "%s-%s" % (self.sessionId, p['name'])

    def prototype(self):
        """Return the prototype info for this component
        as a dictionary of properties with keys 'proto', 'shortname', 'name' and 'id'"""
        
        if vars(self).has_key('_proto'):
            return self._proto
        
        sparql_results = self.query ("""
            select ?proto ?name ?shortname ?id where {

               <%s> austalk:prototype ?proto .
               ?proto austalk:name ?name .
               ?proto austalk:shortname ?shortname .
               ?proto austalk:id ?id .
                
        }""" % (self.identifier,))
        
        self._proto = dict()
        
        for result in sparql_results["results"]["bindings"]:
            self._proto['proto'] = result['proto']['value']
            self._proto['shortname'] = result['shortname']['value']  
            self._proto['name'] = result['name']['value']  
            self._proto['id'] = result['id']['value']      
            return self._proto      


    # Two components are considered equal if they have the same name in the
    # same session
    def __eq__ (self, other):
        return self.session_and_comp_name() == other.session_and_comp_name()

    class Meta:
        app_label= 'search'
        
        
        