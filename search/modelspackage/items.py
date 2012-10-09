from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Item (models.Model):
    """ A item is a logical representation of an item which belongs
    to a component."""

    # Note that id is not specified as this is a Django model
    identifier      = models.URLField ()
    prompt          = models.TextField ()


    @staticmethod
    def filter_by_component (sparql, participant_id, session_id, component_id):
        """ Method returns all the items filtered by the participant/session/component. """
        
        qq = """
            select ?item ?id ?prompt
            where {
                ?rc rdf:type austalk:RecordedComponent .
                ?rc olac:speaker <http://id.austalk.edu.au/participant/%s> .
                ?rc austalk:prototype ?component .
                ?component dc:isPartOf ?session .
                ?session austalk:id %s .
                ?component austalk:shortname "%s" .
                ?item dc:isPartOf ?rc .
                ?item austalk:prototype ?ip .
                ?ip austalk:id ?id .
                ?ip austalk:prompt ?prompt .
        } order by ?id""" % (participant_id, session_id, component_id)
        
        
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query (qq))

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