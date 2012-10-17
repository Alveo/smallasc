from django.db import models

# Models in use
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager

class EducationHistoryManager (SparqlManager):
 

    def filter_by_participant (self, participant):
        """ Returns the EducationHistory of a participant. """
        sparql_results = self.query ("""
            select ?age_from ?age_to ?name
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:education_history ?eh .
                ?eh austalk:age_from ?age_from .
                ?eh austalk:age_to ?age_to .
                ?eh austalk:name ?name .
            FILTER (?part = <%s>) 
            }""" % participant.identifier)

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (EducationHistory (
                                age_from      = result["age_from"]["value"], 
                                age_to        = result["age_to"]["value"],
                                name          = result["name"]["value"]))

        return results


class EducationHistory (SparqlModel):
    """ A participant for a recording session."""

    # custom manager
    objects = EducationHistoryManager ()

    # Field definitions
    age_from          = models.IntegerField ()
    age_to            = models.IntegerField ()
    name              = models.TextField ()


    class Meta:
        app_label= 'search'