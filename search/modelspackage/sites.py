from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Site (models.Model):
    """ A site is a logical representation of the physical location at which
    recording take place."""

    # Field definitions
    identifier          = models.URLField ()
    label               = models.CharField (max_length = 50)
    name                = models.CharField (max_length = 200)
    location            = models.CharField (max_length = 50)
    participant_count   = models.IntegerField ()


    @staticmethod
    def all (sparql):
        """ Returns all the recording locations stored in the rdf store. The endpoint
        and the return format are set by the sparql parameter. The function Returns
        objects of type site. """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""   
            SELECT  ?site ?label ?inst ?city  (count(?part) as ?partcount)
            WHERE {
                ?site rdf:type austalk:RecordingSite .
                ?site austalk:institution ?inst .
                ?site austalk:city ?city .
                ?site rdfs:label ?label .
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site ?site
            }
            group by ?site ?label ?inst ?city"""))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Site (
                                identifier        = result["site"]["value"],
                                label             = result["label"]["value"],
                                name              = result["inst"]["value"],
                                location          = result["city"]["value"],
                                participant_count = int (result["partcount"]["value"])))

        return results


    @staticmethod
    def get (sparql, label):
        """ This function retrieves a site using it's short identifier (not the full url). We do
        not use the full url because placing this in the resource description is a bit ugly."""
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            SELECT  ?site ?inst ?city
            WHERE {
                ?site rdf:type austalk:RecordingSite .
                ?site austalk:institution ?inst .
                ?site austalk:city ?city .
                ?site rdfs:label "%s" .
            }""" % label))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            return Site (
                        identifier        = result["site"]["value"], 
                        name              = result["inst"]["value"],
                        location          = result["city"]["value"])

        return None


    def __unicode__ (self):
        """ Simple name representation for sites """
        return self.name + ', ' + self.location


    class Meta:
        app_label= 'search'