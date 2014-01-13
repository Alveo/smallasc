from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager


class ComponentManager (SparqlManager):

    def get(self, participant_id, session_id, component_id):
        """Return the component for this participant/session/component id
        or None if none exists
        
        participant_id is like 1_123
        session_id is 1, 2, 3
        component_id is shortname words-1, conversation
        """
        
        query = """
            select distinct * where {

                BIND ("%s" AS ?pid)
                BIND (%s as ?sessionid)
                BIND ("%s" as ?shortname)
  
                ?participant austalk:id ?pid .
                ?rc rdf:type austalk:RecordedComponent .
                ?rc olac:speaker ?participant .     
                
            }
        """ % (participant_id, session_id, component_id)

        sparql_results = self.query (query)

        bindings = sparql_results["results"]["bindings"]
        if len(bindings) == 1:
            comp = Component (
                            identifier      = result["rc"]["value"], 
                            participantId   = result["pid"]["value"],
                            sessionId      = result["sessionid"]["value"],
                            )
            comp.details()
            return comp
        else:
            return None
        

    def filter_by_session (self, site_id, participant_id, session_id):
        """ Method returns all the components filtered by the given ids. """

        query = """
            select distinct * where {

                BIND ("%s" AS ?pid)
                BIND (%s as ?sessionid)
  
                ?participant austalk:id ?pid .
                ?rc rdf:type austalk:RecordedComponent .
                ?rc olac:speaker ?participant .     
                
            }
        """ % (participant_id, session_id)


        sparql_results = self.query (query)
        results = []
        for result in sparql_results["results"]["bindings"]:
                comp = Component (
                                identifier      = result["rc"]["value"], 
                                participantId   = result["pid"]["value"],
                                sessionId      = result["sessionid"]["value"],
                                )
                comp.details()
                results.append(comp)
        return results


class Component (SparqlModel):
    """ A component is a logical representation of a component which belongs
    to a session."""

    # custom manager
    objects = ComponentManager ()

    # Note that id is not specified as this is a Django model
    prototype       = models.URLField ()
    name            = models.TextField ()
    site            = models.TextField ()
    componentId     = models.TextField ()
    sessionId       = models.TextField ()
    participantId   = models.TextField ()
    audiorating     = models.TextField ()
    videorating     = models.TextField ()
    comment         = models.TextField ()


    def __unicode__ (self):
        """ Simple name representation for a components """
        return self.name

    def get_absolute_url(self):
        """Return a canonical URL for this item"""                
        return "/browse/%s/%s/%s/%s/" % (self.site, self.participantId, self.sessionId, self.componentId)    

    def session_and_comp_name(self):
        return "%s-%s" % (self.sessionId, self.name)
    
    def details(self):
        """Fill out all details for this component
        based on it's identifier"""
        
        sparql_results = self.query ("""
            select distinct * where {

                BIND (<%s> as ?rc)
                
                ?rc olac:speaker ?participant .
                ?participant austalk:id ?pid .
                ?participant austalk:recording_site ?site .
                ?site rdfs:label ?sitelabel .
                
                ?rc austalk:prototype ?component .
                ?component austalk:shortname ?shortname .
                ?rc dc:isPartOf ?rs .
                ?rs austalk:prototype ?session .
                ?session austalk:id ?sessionid .
                
                ?component austalk:name ?name . 
                OPTIONAL { 
                    ?rc austalk:audiorating ?arating .
                    ?rc austalk:videorating ?vrating .
                    ?rc austalk:comment ?comment .
                }
        }""" % (self.identifier, ))
        
        # we expect one binding
        bindings = sparql_results["results"]["bindings"]
        if len(bindings) == 1:
            bindings = bindings[0]
            self.participantId = bindings['pid']['value']
            self.prototype = bindings['component']['value']
            self.name = bindings['name']['value']
            self.componentId = bindings['shortname']['value']
            self.site = bindings['sitelabel']['value']
            self.sessionId = bindings['sessionid']['value']
            if bindings.has_key('arating'):
                self.audiorating = bindings['arating']['value']
          

    # Two components are considered equal if they have the same name in the
    # same session
    def __eq__ (self, other):
        return self.session_and_comp_name() == other.session_and_comp_name()

    class Meta:
        app_label= 'search'