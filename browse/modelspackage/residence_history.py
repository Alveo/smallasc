from django.db import models

# Models in use
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager

class ResidenceHistoryManager (SparqlManager):
 

    def filter_by_participant (self, participant):
        """ Returns the ResidenceHistory of a participant. """
        query = """
            select distinct ?part ?rh ?age_from ?age_to ?town ?country ?state ?lessyear
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:residential_history ?rh .
                ?rh austalk:age_from ?age_from .
                ?rh austalk:age_to ?age_to .
                ?rh austalk:town ?town .
                ?rh austalk:country ?country .
                ?rh austalk:state ?state .
                ?rh austalk:less_than_a_year ?lessyear .
                FILTER (?part = <%s>) 
            } order by ?age_from""" % participant.identifier
 

        sparql_results = self.query (query)

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (ResidenceHistory (
                                identifier    = result["rh"]["value"],
                                age_from      = result["age_from"]["value"], 
                                age_to        = result["age_to"]["value"],
                                town          = result["town"]["value"],
                                country       = result["country"]["value"],
                                state         = result["state"]["value"],
                                less_than_a_year = result["lessyear"]["value"]))

        return results


class ResidenceHistory (SparqlModel):
    """A place of residence for a participant."""

    # custom manager
    objects = ResidenceHistoryManager ()

    # Field definitions
    age_from          = models.IntegerField ()
    age_to            = models.IntegerField ()
    town              = models.TextField ()
    country           = models.TextField ()
    state             = models.TextField () 
    less_than_a_year  = models.TextField ()

    class Meta:
        app_label= 'search' 