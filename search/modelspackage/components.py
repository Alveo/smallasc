from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Component (models.Model):
    """ A component is a logical representation of a component which belongs
    to a session."""

    # Note that id is not specified as this is a Django model
    identifier      = models.URLField ()
    name            = models.TextField ()
    short_name      = models.TextField ()
    sessionId       = models.IntegerField ()

    @staticmethod
    def all (sparql):
        """ Returns all the session names """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select distinct ?id ?name ?sessId
            where {
                ?comp rdf:type austalk:Component .
                ?comp austalk:id ?id .
                ?comp austalk:name ?name .
                ?comp dc:isPartOf ?session .
                ?session rdf:type austalk:Session .
                ?session austalk:id ?sessId .
                FILTER (?sessId in (1, 2)) .
            }
            ORDER BY ?name"""))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                id = result["id"]["value"], 
                                name = result["name"]["value"],
                                sessionId = result["sessId"]["value"]))

        return results


    @staticmethod
    def filter_by_session (sparql, session):
        """ Method returns all the components filtered by the session. """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select ?component ?id ?name ?shortname
            where {
                ?component rdf:type austalk:Component .
                ?component austalk:name ?name .
                ?component austalk:shortname ?shortname .
                ?component austalk:id ?id .
                ?component dc:isPartOf <%s> .
        }""" % session.identifier))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Component (
                                identifier      = result["component"]["value"], 
                                id              = result["id"]["value"], 
                                name            = result["name"]["value"],
                                short_name      = result["shortname"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for a components """
        return self.name


    class Meta:
        app_label= 'search'