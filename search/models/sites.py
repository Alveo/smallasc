from django.db import models

class Sites (models.Model):
    """ A site is a logical representation of the physical location at which
    recording take place."""

    name = models.CharField (max_length = 200)
    location = models.CharField (max_length = 50)
    site = models.TextField ()

    @staticmethod
    def all (sparql):
        """ Returns all the recording locations stored in the rdf store. The endpoint
        and the return format are set by the sparql parameter. The function Returns
        objects of type site. """
        sparql.setQuery ("""
            PREFIX austalk:<http://ns.austalk.edu.au/>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT distinct ?site ?city ?inst
            WHERE {
                ?site rdf:type austalk:RecordingSite .
                ?site austalk:city ?city .
                ?site austalk:institution ?inst .}""")

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Sites (
                                site = result["site"]["value"], 
                                name = result["inst"]["value"],
                                location = result["city"]["value"]))

        return results


    def __unicode__ (self):
        """ Simple name representation for sites """
        return self.name + ', ' + self.location


    class Meta:
        app_label= 'search'