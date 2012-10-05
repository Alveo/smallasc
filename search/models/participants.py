from django.db import models
from search.models.sparql_local_wrapper import SparqlLocalWrapper


class Participants (models.Model):
    """ A participant for a recording session."""

    # Field definitions
    identifier        = models.TextField ()
    gender            = models.CharField (max_length = 50)
    birth_year        = models.IntegerField ()


    @staticmethod
    def all (sparql, site):
        """ Returns all the recording locations stored in the rdf store. The endpoint
        and the return format are set by the sparql parameter. The function Returns
        objects of type site. """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select ?part ?gender ?dob
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site <%s> .
                ?part foaf:gender ?gender .
                ?part dbpedia:birthYear ?dob .
            }""" % site.identifier))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Participants (
                                identifier          = result["part"]["value"], 
                                gender              = result["gender"]["value"],
                                birth_year          = result["dob"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for sites """
        # TODO: Need to convert this to animal/colour
        return identifier


    class Meta:
        app_label= 'participants'