import re

from django.db                                  import models
from urlparse                                   import urlsplit

from baseapp.modelspackage.colours              import Colour
from baseapp.modelspackage.animals              import Animal
from browse.modelspackage.sparql_local_wrapper  import SparqlModel, SparqlManager


class ParticipantManager (SparqlManager):

    def all (self, site):

        sparql_results = self.query("""
            select ?part ?gender ?dob
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site <%s> .
                ?part foaf:gender ?gender .
                ?part dbpedia:birthYear ?dob .
            }""" % site.identifier)

        results = []

        for result in sparql_results["results"]["bindings"]:
            
            part = Participant (
                identifier          = result["part"]["value"], 
                gender              = result["gender"]["value"],
                birth_year          = result["dob"]["value"]
            )

            results.append (part)


        return results


    def with_data (self, site, limit=1000, offset=0):
        
        sparql_results = self.query ("""
            select distinct ?part 
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site <%s> . 
                ?rs olac:speaker ?part .
                ?rs rdf:type austalk:RecordedSession .
            } LIMIT %d OFFSET %d""" % (site.identifier, limit, offset))

        results = []

        for result in sparql_results["results"]["bindings"]:

            part = Participant (identifier = result["part"]["value"])
            results.append(part)

        return results


    def get (self, participant_id):

        qq = """
            select  ?part ?prop ?value
            where {
                ?part rdf:type foaf:Person .
                ?part ?prop ?value .

                FILTER (?part = <http://id.austalk.edu.au/participant/%s>)
            }""" % participant_id        

        sparql_results = self.query (qq)

        for result in sparql_results["results"]["bindings"]:
            return Participant(identifier = result["part"]["value"])
                        
        return None


    def filter (self, predicates = {}):

        qq = """
            select  distinct ?part
            where {
                ?part rdf:type foaf:Person .
            """
        for (key,value) in predicates.items():
            qq += """ ?part """ + key + " '" + value + "' . "

        qq += """}"""

        print qq
        
        sparql_results = self.query (qq)

        results = []
        
        for result in sparql_results["results"]["bindings"]:
            results.append (Participant(identifier = result["part"]["value"]))
                        
        return results


class Participant (SparqlModel):

    # custom manager
    objects = ParticipantManager()


    def get_name(self):
        return self.properties()['name'][0]


    def get_site(self):

        site_url        = self.properties()['recording_site'][0]
        site_path       = urlsplit(site_url).path
        path_components = site_path.split('/')

        return path_components[len(path_components) - 1]


    # Fields
    name = property(get_name)
    site = property(get_site)

  
    def get_absolute_url(self):
        return "/browse/%s/%s" % (self.site.label, self.friendly_id ())


    def friendly_id (self):
        return self.properties()['id'][0]


    def __unicode__ (self):
        return self.properties()['id'][0] + " (" + self.properties()['name'][0] + ")"
    

    def __eq__ (self, other):
        return self.friendly_id () == other.friendly_id ()


    class Meta:
        app_label= 'search'