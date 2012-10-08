from django.db import models

# Models in use
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class EducationHistory (models.Model):
    """ A participant for a recording session."""

    # Field definitions
    age_from          = models.IntegerField ()
    age_to            = models.IntegerField ()
    name              = models.TextField ()


    @staticmethod
    def filter_by_participant (sparql, participant):
        """ Returns the EducationHistory of a participant. """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select ?age_from ?age_to ?name
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:education_history ?eh .
                ?eh austalk:age_from ?age_from .
                ?eh austalk:age_to ?age_to .
                ?eh austalk:name ?name .
            FILTER (?part = <%s>) 
            }""" % participant.identifier))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (EducationHistory (
                                age_from      = result["age_from"]["value"], 
                                age_to        = result["age_to"]["value"],
                                name          = result["name"]["value"]))

        return results


    class Meta:
        app_label= 'search'