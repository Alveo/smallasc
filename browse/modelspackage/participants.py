import re
from django.db import models
from urlparse import urlparse

# Models in use
from baseapp.modelspackage.colours import Colour
from baseapp.modelspackage.animals import Animal
from browse.modelspackage.locations import Location
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager


class ParticipantManager (SparqlManager):

    def all (self, site):
        """ Returns all the participants stored in the rdf store as instances of Participant. """
        sparql_results = self.query ("""
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
                                birth_year          = result["dob"]["value"])
            part.set_site (site)
            results.append (part)

        return results


    def with_data (self, site):
        """ Returns all the participants who have at least one session as a list of instances
        of Participant """
        
        sparql_results = self.query ("""
            select distinct ?part 
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site <%s> . 
                ?rs olac:speaker ?part .
                ?rs rdf:type austalk:RecordedSession .
            }""" % site.identifier)

        results = []

        for result in sparql_results["results"]["bindings"]:
            part = Participant (identifier = result["part"]["value"])
            part.set_site (site)
            results.append (part)

        return results


    def get (self, participant_id):
        """ This function returns the particulars of a participant. """
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
                        
        #print "Participant not found", participant_id
        return None


    def filter (self, predicates = {}):
        """ 
            This method filters participants using a hash of predicates. Perhaps we
            should push this method up the class heirarchy?
        """
        qq = """
            select  distinct ?part
            where {
                ?part rdf:type foaf:Person .
            """
        for (key,value) in predicates.items():
            qq += """ ?part """ + key + " '" + value + "' . "

        qq += """}"""

        sparql_results = self.query (qq)
        results = []
        for result in sparql_results["results"]["bindings"]:
            results.append (Participant(identifier = result["part"]["value"]))
                        
        return results


class Participant (SparqlModel):
    """ A participant for a recording session."""

    # custom manager
    objects = ParticipantManager()

    # Associations
    site = None

    # Setter
    def set_site (self, site):
        self.site = site

  
    def get_absolute_url(self):
        """Return a canonical URL for this item"""    
        return "/browse/%s/%s" % (self.site.label, self.friendly_id ())


    def friendly_id (self):
        """ This function converts the participants fully qualified id into something shorter. """
        return self.properties()['id'][0]


    def __unicode__ (self):
        """ Simple name representation for sites """
        return self.properties()['id'][0] + " (" + self.properties()['name'][0] + ")"
    

    def __eq__ (self, other):
        return self.friendly_id () == other.friendly_id ()


    class Meta:
        app_label= 'search'