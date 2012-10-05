from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Session (models.Model):
    """ A session is a logical representation of the actual recording session
    which takes place at a particular location."""
    # Note that id is not specified as this is a Django model
    name = models.CharField (max_length = 50)

    @staticmethod
    def all (sparql):
        """ Returns all the session names """
        sparql.setQuery (SparqlLocalWrapper.canonicalise_query ("""
            select distinct ?id ?name 
            where {
                ?session rdf:type austalk:Session .
                ?session austalk:id ?id .
                ?session austalk:name ?name .
            }
            ORDER BY ?name"""))

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Session (
                                id = result["id"]["value"], 
                                name = result["name"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for a session """
        return self.name


    class Meta:
        app_label = 'search'