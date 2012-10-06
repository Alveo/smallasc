import re
from django.db import models
from urlparse import urlparse

# Models in use
from baseapp.modelspackage.colours import Colour
from baseapp.modelspackage.animals import Animal
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Participant (models.Model):
    """ A participant for a recording session."""

    # Field definitions
    identifier        = models.URLField ()
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
            results.append (Participant (
                                identifier          = result["part"]["value"], 
                                gender              = result["gender"]["value"],
                                birth_year          = result["dob"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for sites """
        
        url_scheme = urlparse (self.identifier)
        (colour_id, animal_id) = re.findall ('\d+', url_scheme.path)
        colour = Colour.objects.get (id = colour_id)
        animal = Animal.objects.get (id = animal_id)
        return '%s - %s (%s_%s)' % (colour.name, animal.name, colour_id, animal_id)


    class Meta:
        app_label= 'search'