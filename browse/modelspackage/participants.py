import re

from django.db                                  import models
from urlparse                                   import urlsplit

from baseapp.modelspackage.colours              import Colour
from baseapp.modelspackage.animals              import Animal
from browse.modelspackage.sparql_local_wrapper  import SparqlModel, SparqlManager


class ParticipantManager (SparqlManager):

    def all (self, site):
        print ('site --------- ', site)
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
                identifier          = result["part"]["value"]
                #gender              = result["gender"]["value"],
                #birth_year          = result["dob"]["value"]
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

        # include olac:recorder here to make sure this is a
        # participant and not an RA
        qq = """
            select  distinct ?part
            where {
                ?part rdf:type foaf:Person .
                ?part olac:recorder ?someone .
            """
        for (key,value) in predicates.items():
            # kludge to handle URIs as values (eg. recording site)
            if value.startswith('<') and value.endswith('>'):
                qq += """\t?part """ + key + " " + value + " . \n"
            else:
                qq += """\t?part """ + key + " '" + value + "' . \n"

        qq += """}"""

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

        if 'recording_site' in self.properties():
            site_url        = self.properties()['recording_site'][0]
        else:
            return "/unknown_participant"
        site_path       = urlsplit(site_url).path
        path_components = site_path.split('/')

        return path_components[len(path_components) - 1]


    def get_web_video(self):
        """Return the URL of the sample video for this participant"""

        qq = """select ?video where {
   ?item austalk:componentName "story" .
   ?item olac:speaker <%s> .
   ?item ausnc:document ?video .
   ?video dc:type "video" .
}""" % self.identifier

        sparql_results = self.query (qq)

        for result in sparql_results["results"]["bindings"]:
            return result["video"]["value"]

        return None


    # Fields
    name = property(get_name)
    site = property(get_site)


    def get_absolute_url(self):
        return "/browse/%s/%s" % (self.site, self.friendly_id ())


    def friendly_id (self):
        return self.properties()['id'][0]


    def __unicode__ (self):
        return self.properties()['id'][0] + " (" + self.properties()['name'][0] + ")"


    def __eq__ (self, other):
        return self.friendly_id () == other.friendly_id ()


    class Meta:
        app_label= 'search'
