from django.db import models

class Sites (models.Model):
    """ A site is a logical representation of the physical location at which
    recording take place."""

    # Field definitions
    name                = models.CharField (max_length = 200)
    location            = models.CharField (max_length = 50)
    site                = models.TextField ()
    participant_count   = models.IntegerField ()


    @staticmethod
    def all (sparql):
        """ Returns all the recording locations stored in the rdf store. The endpoint
        and the return format are set by the sparql parameter. The function Returns
        objects of type site. """
        sparql.setQuery ("""
            PREFIX foaf:<http://xmlns.com/foaf/0.1/>
            PREFIX austalk:<http://ns.austalk.edu.au/>
            PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT  ?site ?inst ?city  (count(?part) as ?partcount)
            WHERE {
                ?site rdf:type austalk:RecordingSite .
                ?site austalk:institution ?inst .
                ?site austalk:city ?city .
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site ?site
            }
            group by ?site ?inst ?city""")

        sparql_results = sparql.query ().convert ()
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Sites (
                                site              = result["site"]["value"], 
                                name              = result["inst"]["value"],
                                location          = result["city"]["value"],
                                participant_count = int (result["partcount"]["value"])))

        return results


    def __unicode__ (self):
        """ Simple name representation for sites """
        return self.name + ', ' + self.location


    class Meta:
        app_label= 'sites'