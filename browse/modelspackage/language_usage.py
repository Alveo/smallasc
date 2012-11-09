from django.db import models

# Models in use
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager

class LanguageUsageManager (SparqlManager):


    def filter_by_participant (self, participant):
        """ Returns the Language Use of a participant. """
        query = """
            select ?name ?sit ?freq
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:language_usage ?lu .
                ?lu austalk:situation ?sit .
                ?lu austalk:frequency ?freq . 
                ?lu austalk:name ?name .
            FILTER (?part = <%s>) 
            }""" % participant.identifier
            
        print query
        
        sparql_results = self.query (query)

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (LanguageUsage (
                                situation            = result["sit"]["value"], 
                                frequency            = result["freq"]["value"], 
                                name                 = result["name"]["value"]))

        return results


class LanguageUsage (SparqlModel):
    """ A participant for a recording session."""

    # custom manager
    objects = LanguageUsageManager ()

    # Field definitions 
    name              = models.TextField ()
    situation         = models.TextField ()
    frequency         = models.TextField ()


    class Meta:
        app_label= 'search'