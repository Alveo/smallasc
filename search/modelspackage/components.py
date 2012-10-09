from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Component (models.Model):
    """ A component is a logical representation of a component which belongs
    to a session."""

    # Note that id is not specified as this is a Django model
    identifier      = models.URLField ()
    prototype       = models.URLField ()
    name            = models.TextField ()
    short_name      = models.TextField ()

    @staticmethod
    def all (sparql):
        """ Returns all the session names """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select distinct ?comp ?proto ?name ?shortname 
            where {
                ?comp rdf:type austalk:RecordedComponent .
                ?comp austalk:prototype ?proto .
                ?proto austalk:name ?name .
                ?proto austalk:shortname ?shortname .
            }
            ORDER BY ?name"""))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                identifier = result["comp"]["value"], 
                                prototype = result["comp"]["value"],
                                name = result["name"]["value"],
                                short_name = result["shortname"]["value"]))

        return results
    
    @staticmethod 
    def get(sparql, participant_id, session_id, component_id):
        """Return the component for this participant/session/component id
        
        participant_id is like 1_123
        session_id is 1, 2, 3
        component_id is shortname words-1, conversation
        """
        
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select ?rc ?component ?name
            where {
                ?rc rdf:type austalk:RecordedComponent .
                ?rc olac:speaker <http://id.austalk.edu.au/participant/%s> .
                ?rc austalk:prototype ?component .
                ?component dc:isPartOf ?session .
                ?session austalk:id %s .
                ?component austalk:name ?name .
                ?component austalk:shortname "%s" . 
        }""" % (participant_id, session_id, component_id)))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                identifier      = result["rc"]["value"], 
                                prototype       = result["component"]["value"], 
                                name            = result["name"]["value"],
                                short_name      = component_id))

        return results   
        

    @staticmethod
    def filter_by_session (sparql, session):
        """ Method returns all the components filtered by the session. """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select ?rc ?component ?name ?shortname
            where {
                ?rc rdf:type austalk:RecordedComponent .
                ?rc dc:isPartOf <%s> .
                ?rc austalk:prototype ?component .
                ?component austalk:name ?name .
                ?component austalk:shortname ?shortname . 
        }""" % session.identifier))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                identifier      = result["rc"]["value"], 
                                prototype       = result["component"]["value"], 
                                name            = result["name"]["value"],
                                short_name      = result["shortname"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for a components """
        return self.name


    class Meta:
        app_label= 'search'