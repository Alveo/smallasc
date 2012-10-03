from django.db import models

class Components (models.Model):
    """ A component is a logical representation of a component which belongs
    to a session."""
    # Note that id is not specified as this is a Django model
    name = models.CharField (max_length = 50)
    sessionId = models.IntegerField ()

    @staticmethod
    def all (sparql):
        """ Returns all the session names """
        sparql.setQuery ("""
            PREFIX dc: <http://purl.org/dc/terms/>
            PREFIX austalk:<http://ns.austalk.edu.au/>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            select distinct ?id ?name ?sessId
            where {
                ?comp rdf:type austalk:Component .
                ?comp austalk:id ?id .
                ?comp austalk:name ?name .
                ?comp dc:isPartOf ?session .
                ?session rdf:type austalk:Session .
                ?session austalk:id ?sessId .
                FILTER (?sessId in (1, 2)) .
            }
            ORDER BY ?name""")

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Components (
                                id = result["id"]["value"], 
                                name = result["name"]["value"],
                                sessionId = result["sessId"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for a components """
        return self.name


    class Meta:
        app_label= 'components'