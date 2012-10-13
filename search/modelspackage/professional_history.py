from django.db import models

# Models in use
from search.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager

class ProfessionalHistoryManager (SparqlManager):


    def filter_by_participant (self, participant):
        """ Returns the EducationHistory of a participant. """
        sparql_results = self.query ("""
            select ?age_from ?age_to ?less_than_a_year ?name
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:profession_history ?ph .
                ?ph austalk:age_from ?age_from .
                ?ph austalk:age_to ?age_to .
                ?ph austalk:less_than_a_year ?less_than_a_year .
                ?ph austalk:name ?name .
            FILTER (?part = <%s>) 
            }""" % participant.identifier)

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (ProfessionalHistory (
                                age_from            = result["age_from"]["value"], 
                                age_to              = result["age_to"]["value"],
                                less_than_a_year    = result["less_than_a_year"]["value"],
                                name                = result["name"]["value"]))

        return results


class ProfessionalHistory (SparqlModel):
    """ A participant for a recording session."""

    # Field definitions
    age_from          = models.IntegerField ()
    age_to            = models.IntegerField ()
    less_than_a_year  = models.BooleanField ()
    name              = models.TextField ()


    class Meta:
        app_label= 'search'