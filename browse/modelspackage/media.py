from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Media (models.Model):

    # Note that id is not specified as this is a Django model
    identifier          = models.URLField ()

    @staticmethod
    def filter_by_componentitems (sparql, component, item):
        """ Method returns all the media filtered by the item. """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select ?media
            where {
                ?ausnc rdf:type ausnc:AusNCObject .
                ?ausnc austalk:basename ?basename .
                ?ausnc austalk:media ?media .
                ?ausnc austalk:prototype ?item .
                ?ausnc dc:isPartOf ?isPartOf .
                FILTER (?isPartOf = <%s>) .
                FILTER (?item = <%s>) .
            }""" % (component.identifier, item.identifier)))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Media (identifier = result["media"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for a media file is it's url """
        return self.identifier


    class Meta:
        app_label= 'search'