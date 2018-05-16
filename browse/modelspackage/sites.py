from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager
from browse.modelspackage           import Session
from collections import defaultdict


class SiteManager (SparqlManager):
    """ Class responsible for returning instances of type Site. """

    def all (self):
        """ Returns all the recording locations stored in the rdf store. The endpoint
        and the return format are set by the sparql parameter. The function Returns
        objects of type site. """
        sparql_results = self.query ("""
            SELECT  distinct ?site ?label ?inst ?city  (count(distinct ?part) as ?partcount)
            WHERE {
                ?site rdf:type austalk:RecordingSite .
                ?site austalk:institution ?inst .
                ?site austalk:city ?city .
                ?site rdfs:label ?label .
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site ?site
            }
            group by ?site ?label ?inst ?city""")

        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Site (
                                client            = self.client,
                                identifier        = result["site"]["value"],
                                label             = result["label"]["value"],
                                name              = result["inst"]["value"],
                                location          = result["city"]["value"],
                                participant_count = int (result["partcount"]["value"])))

        return results

    def all_site_and_session_counts(self):
        """ Returns a list containing a dictionary of the different site and 
        session combinations along with the participant count for that combo."""
        sparql_results = self.query ("""
            SELECT (SAMPLE(?label) as ?LABEL) (SAMPLE(?number) as ?SESSION) (COUNT(?pid) as ?NPID)
            WHERE {
                ?rs rdf:type austalk:RecordedSession .
                ?rs olac:speaker ?participant .
                
                ?participant austalk:id ?pid .
                ?participant austalk:recording_site ?site .
                ?site rdfs:label ?label .
                
                ?rs austalk:prototype ?session .
                  ?session austalk:id ?number .
            }
            GROUP BY ?label ?session""")

        results = {}

        for result in sparql_results["results"]["bindings"]:
            #The first key is the site
            site = result["LABEL"]["value"]
            session = result["SESSION"]["value"]
            count = result["NPID"]["value"]
            if not site in results:
                results[site] = {}
            results[site][session] = count

        return results

    def get (self, label):
        """ This function retrieves a site using it's short identifier (not the full url). We do
        not use the full url because placing this in the resource description is a bit ugly."""
        sparql_results = self.query ("""
            SELECT distinct ?site ?inst ?city
            WHERE {
                ?site rdf:type austalk:RecordingSite .
                ?site austalk:institution ?inst .
                ?site austalk:city ?city .
                ?site rdfs:label "%s" .
            }""" % label)

        results = []

        for result in sparql_results["results"]["bindings"]:
            return Site (
                        client            = self.client,
                        identifier        = result["site"]["value"],
                        name              = result["inst"]["value"],
                        location          = result["city"]["value"])

        return None


class Site (SparqlModel):
    """ A site is a logical representation of the physical location at which
    recording take place."""

    # custom manager
    objects = SiteManager ()

    # Field definitions
    label               = models.TextField ()
    name                = models.TextField ()
    location            = models.TextField ()
    participant_count   = models.IntegerField ()

    def stats(self):
        """Return some statistics for this site"""

        q = """select ?gender (count(distinct ?part) as ?count) where {
        BIND (<%s> AS ?site)

        ?part austalk:recording_site ?site .
        ?part foaf:gender ?gender .

 } group by ?gender
        """ % (self.identifier,)

        results = self.query(q)

        self.__stats = dict()

        for result in results["results"]["bindings"]:
            self.__stats[result["gender"]["value"]] =  result["count"]["value"]

        return self.__stats

    def session_stats(self,sessionManager):
        """Return session statistics (no. of recordings in each session) for this site
            {
                '1': 49,
                '2': 24,
                '3': 20,
                '4': 15
            }
        """
        data = defaultdict(int)
        sessions = sessionManager.filter_by_site(self.label)
        for session in sessions:
            data[session.number] += 1

        return data

    def get_absolute_url(self):
        """Return a canonical URL for this item"""
        return "/browse/%s/" % (self.label)


    def __unicode__ (self):
        """ Simple name representation for sites """
        return self.name + ', ' + self.location


    class Meta:
        app_label= 'search'
