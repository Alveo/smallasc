from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager


class ComponentManager (SparqlManager):

    def all (self):
        """ Returns all the component names """
        sparql_results = self.query ("""
            select distinct ?rc ?proto ?name ?shortname ?arating ?vrating ?comment
            where {
                ?rc rdf:type austalk:RecordedComponent .
                ?rc austalk:prototype ?proto .
                ?proto austalk:name ?name .
                ?proto austalk:shortname ?shortname .
                OPTIONAL { 
                ?rc austalk:audiorating ?arating .
                ?rc austalk:videorating ?vrating .
                ?rc austalk:comment ?comment .
                }
            }
            ORDER BY ?name""")


        return self.generate_component_list(sparql_results)
    

    def get(self, participant_id, session_id, component_id):
        """Return the component for this participant/session/component id
        
        participant_id is like 1_123
        session_id is 1, 2, 3
        component_id is shortname words-1, conversation
        """
        
        qpart = """
                BIND ("%s" AS ?pid)
                BIND (%s as ?sessionid)
                BIND ("%s" as ?shortname)
            """ % (participant_id, session_id, component_id)

        return self.generate_component_list(sparql_results)
        

    def filter_by_session (self, site_id, participant_id, session_id):
        """ Method returns all the components filtered by the given ids. """
        qpart = """
                BIND ("%s" AS ?pid)
                BIND (%s as ?sessionid)
                """ % (participant_id, session_id)

        return self.generate_component_list(qpart)


    def generate_component_list(self, qpart):
        
        
        sparql_results = self.query ("""
            select distinct * where {

                %s
                
                ?rc rdf:type austalk:RecordedComponent .
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
        }""" % (qpart,))
        
        results = []

        for result in sparql_results["results"]["bindings"]:
            if result.has_key("arating"):
                results.append (Component (
                                identifier      = result["rc"]["value"], 
                                prototype       = result["component"]["value"], 
                                name            = result["name"]["value"],
                                componentId      = result["shortname"]["value"],
                                sessionId      = result["sessionid"]["value"],
                                site            = result["sitelabel"]["value"],
                                participantId   = result["pid"]["value"],
                                audiorating     = result["arating"]["value"],
                                videorating     = result["vrating"]["value"],
                                comment         = result["comment"]["value"]
                                )
                                )
            else:
                results.append (Component (
                                identifier      = result["rc"]["value"], 
                                prototype       = result["component"]["value"], 
                                name            = result["name"]["value"],
                                componentId     = result["shortname"]["value"],
                                site            = result["sitelabel"]["value"],
                                participantId   = result["pid"]["value"],
                                sessionId      = result["sessionid"]["value"],
                                ))
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

    

    class Meta:
        app_label= 'search'