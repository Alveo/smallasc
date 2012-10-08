from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Item (models.Model):
    """ A item is a logical representation of an item which belongs
    to a component."""

    # Note that id is not specified as this is a Django model
    identifier      = models.URLField ()
    prompt            = models.TextField ()


    @staticmethod
    def filter_by_component (sparql, component):
        """ Method returns all the items filtered by the component. """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select ?item ?id ?prompt
            where {
                ?component rdf:type austalk:Component .
                ?item rdf:type austalk:Item .
                ?item austalk:id ?id .
                ?item austalk:prompt ?prompt .
                ?item dc:isPartOf ?component .
                FILTER (?component = <%s>)
            }""" % component.identifier))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Item (
                                identifier      = result["item"]["value"], 
                                id              = result["id"]["value"], 
                                prompt            = result["prompt"]["value"]))

        return results


    class Meta:
        app_label= 'search'