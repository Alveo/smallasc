from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager


class ComponentManager (SparqlManager):

    def all (self):
        """ Returns all the session names """
        sparql_results = self.query ("""
            select distinct ?comp ?proto ?name ?shortname 
            where {
                ?comp rdf:type austalk:RecordedComponent .
                ?comp austalk:prototype ?proto .
                ?proto austalk:name ?name .
                ?proto austalk:shortname ?shortname .
            }
            ORDER BY ?name""")

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                identifier = result["comp"]["value"], 
                                prototype = result["comp"]["value"],
                                name = result["name"]["value"],
                                short_name = result["shortname"]["value"]))

        return results
    

    def get(sparql, component):
        """Return the component for this participant/session/component id
        
        participant_id is like 1_123
        session_id is 1, 2, 3
        component_id is shortname words-1, conversation
        """
        
        sparql_results = self.query ("""
            select ?rc ?component ?name
            where {
                ?rc rdf:type austalk:RecordedComponent .
                ?rc austalk:prototype ?component .
                ?component dc:isPartOf ?session .
                ?component austalk:name ?name .
                ?component austalk:id <%s> . 
        }""" % (component.identifier))

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                identifier      = result["rc"]["value"], 
                                prototype       = result["component"]["value"], 
                                name            = result["name"]["value"],
                                short_name      = component_id))

        return results   
        

    def filter_by_session (self, session):
        """ Method returns all the components filtered by the session. """
        sparql_results = self.query ("""
            select ?rc ?component ?name ?shortname
            where {
                ?rc rdf:type austalk:RecordedComponent .
                ?rc dc:isPartOf <%s> .
                ?rc austalk:prototype ?component .
                ?component austalk:name ?name .
                ?component austalk:shortname ?shortname . 
        }""" % session.identifier)

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                identifier      = result["rc"]["value"], 
                                prototype       = result["component"]["value"], 
                                name            = result["name"]["value"],
                                short_name      = result["shortname"]["value"]))

        return results


class Component (SparqlModel):
    """ A component is a logical representation of a component which belongs
    to a session."""

    # custom manager
    objects = ComponentManager ()

    # Note that id is not specified as this is a Django model
    prototype       = models.URLField ()
    name            = models.TextField ()
    short_name      = models.TextField ()


    def __unicode__ (self):
        """ Simple name representation for a components """
        return self.name


    class Meta:
        app_label= 'search'