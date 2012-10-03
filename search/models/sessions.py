from django.db import models

class Sessions (models.Model):
    """ A session is a logical representation of the actual recording session
    which takes place at a particular location."""
    # Note that id is not specified as this is a Django model
    name = models.CharField (max_length = 50)

    @staticmethod
    def all (sparql):
        """ Returns all the session names """
        sparql.setQuery ("""
            PREFIX austalk:<http://ns.austalk.edu.au/>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            select distinct ?id ?name 
            where {
                ?session rdf:type austalk:Session .
                ?session austalk:id ?id .
                ?session austalk:name ?name .
            }
            ORDER BY ?name""")

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Sessions (
                                id = result["id"]["value"], 
                                name = result["name"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for a session """
        return self.name


    class Meta:
        app_label = 'sessions'