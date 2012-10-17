import re
from django.db import models
from urlparse import urlparse

# Models in use
from baseapp.modelspackage.colours import Colour
from baseapp.modelspackage.animals import Animal
from search.modelspackage.locations import Location
from search.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager


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
            select ?part ?gender ?dob
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site <%s> .
                ?part foaf:gender ?gender .
                ?part dbpedia:birthYear ?dob .
                ?rs olac:speaker ?part .
                ?rs rdf:type austalk:RecordedSession .
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




    def get (self, participant_id):
        """ This function returns the particulars of a participant. """
        qq = """
            select  ?part ?gender ?dob ?birthPlace ?cultural_heritage ?hobbies_details ?religion 
                    ?first_language ?other_languages 
                    ?mother_cultural_heritage ?mother_first_language ?mother_accent ?mother_professional_category ?mother_education_level ?mother_pob_town ?mother_pob_state ?mother_pob_country
                    ?father_cultural_heritage ?father_first_language ?father_accent ?father_professional_category ?father_education_level ?father_pob_town ?father_pob_state ?father_pob_country
                    ?has_reading_problems ?has_vocal_training ?has_speech_problems ?has_hearing_problems ?is_left_handed
                    ?is_smoker ?has_dentures ?has_piercings ?has_health_problems
            where {
                ?part rdf:type foaf:Person .
                ?part austalk:recording_site ?site .
                ?part foaf:gender ?gender .
                ?part dbpedia:birthYear ?dob .
                ?part austalk:birthPlace ?birthPlace .
                ?part austalk:cultural_heritage ?cultural_heritage .
                ?part austalk:hobbies_details ?hobbies_details .
                ?part austalk:religion ?religion .
                ?part austalk:first_language ?first_language .
                ?part austalk:other_languages ?other_languages .

                ?part austalk:mother_cultural_heritage ?mother_cultural_heritage .
                ?part austalk:mother_pob_town ?mother_pob_town .
                ?part austalk:mother_pob_state ?mother_pob_state .
                ?part austalk:mother_pob_country ?mother_pob_country .
                ?part austalk:mother_first_language ?mother_first_language .
                ?part austalk:mother_accent ?mother_accent .
                ?part austalk:mother_professional_category ?mother_professional_category .
                ?part austalk:mother_education_level ?mother_education_level .

                ?part austalk:father_cultural_heritage ?father_cultural_heritage .
                ?part austalk:father_pob_town ?father_pob_town .
                ?part austalk:father_pob_state ?father_pob_state .
                ?part austalk:father_pob_country ?father_pob_country .
                ?part austalk:father_first_language ?father_first_language .
                ?part austalk:father_accent ?father_accent .
                ?part austalk:father_professional_category ?father_professional_category .
                ?part austalk:father_education_level ?father_education_level .

                ?part austalk:has_reading_problems ?has_reading_problems .
                ?part austalk:has_vocal_training ?has_vocal_training .
                ?part austalk:has_speech_problems ?has_speech_problems .
                ?part austalk:has_hearing_problems ?has_hearing_problems .
                ?part austalk:is_left_handed ?is_left_handed .
                ?part austalk:is_smoker ?is_smoker .
                ?part austalk:has_dentures ?has_dentures .
                ?part austalk:has_piercings ?has_piercings .
                ?part austalk:has_health_problems ?has_health_problems .

                FILTER (?part = <http://id.austalk.edu.au/participant/%s>)
            }""" % participant_id
            
        qq = """
            select  ?part ?prop ?value
            where {
                ?part rdf:type foaf:Person .
                ?part ?prop ?value .

                FILTER (?part = <http://id.austalk.edu.au/participant/%s>)
            }""" % participant_id
        

        sparql_results = self.query(qq)

        for result in sparql_results["results"]["bindings"]:
            print result
            return Participant(identifier = result["part"]["value"])
            
            mother_pob = Location (
                            town    = result["mother_pob_town"]["value"],
                            state   = result["mother_pob_state"]["value"],
                            country = result["mother_pob_country"]["value"])

            father_pob = Location (
                            town    = result["father_pob_town"]["value"],
                            state   = result["father_pob_state"]["value"],
                            country = result["father_pob_country"]["value"])

            return Participant (
                        identifier              = result["part"]["value"], 
                        gender                  = result["gender"]["value"],
                        birth_year              = result["dob"]["value"],
                        birth_place             = result["birthPlace"]["value"],
                        cultural_heritage       = result["cultural_heritage"]["value"],
                        hobbies_details         = result["hobbies_details"]["value"],
                        religion                = result["religion"]["value"],
                        first_language          = result["first_language"]["value"],
                        other_languages         = result["other_languages"]["value"],

                        mother_cultural_heritage= result["mother_cultural_heritage"]["value"],
                        mother_pob_location     = mother_pob,
                        mother_first_language   = result["mother_first_language"]["value"],
                        mother_accent           = result["mother_accent"]["value"],
                        mother_occupation       = result["mother_professional_category"]["value"],
                        mother_education_level  = result["mother_education_level"]["value"],

                        father_cultural_heritage= result["father_cultural_heritage"]["value"],
                        father_pob_location     = father_pob,
                        father_first_language   = result["father_first_language"]["value"],
                        father_accent           = result["father_accent"]["value"],
                        father_occupation       = result["father_professional_category"]["value"],
                        father_education_level  = result["father_education_level"]["value"],

                        has_reading_problems    = result["has_reading_problems"]["value"],
                        has_vocal_training      = result["has_vocal_training"]["value"],
                        has_speech_problems     = result["has_speech_problems"]["value"],
                        has_hearing_problems    = result["has_hearing_problems"]["value"],
                        is_left_handed          = result["is_left_handed"]["value"],
                        is_smoker               = result["is_smoker"]["value"],
                        has_dentures            = result["has_dentures"]["value"],
                        has_piercings           = result["has_piercings"]["value"],
                        has_health_problems     = result["has_health_problems"]["value"])

        print "Participant not found", participant_id
        return None


class Participant (SparqlModel):
    """ A participant for a recording session."""


    # custom manager
    objects = ParticipantManager()
    
    # Field definitions, note the use of lots of test fields. This is
    # because at present the data is persisted in a RDF store so we
    # don't care about the specifics of the types so much, we only care
    # about basic type correctness
    gender                      = models.TextField ()
    birth_year                  = models.IntegerField ()
    birth_place                 = models.TextField ()
    cultural_heritage           = models.TextField ()
    hobbies_details             = models.TextField ()
    religion                    = models.TextField ()
    first_language              = models.TextField ()
    other_languages             = models.TextField ()

    # Mother details
    mother_cultural_heritage    = models.TextField ()

    # We do not want a backwards relation from location
    mother_pob_location         = models.ForeignKey (Location, related_name = '+')
    mother_first_language       = models.TextField ()
    mother_accent               = models.TextField ()
    mother_occupation           = models.TextField ()
    mother_education_level      = models.TextField ()

    # Father details
    father_cultural_heritage    = models.TextField ()

    # We do not want a backwards relation from location
    father_pob_location         = models.ForeignKey (Location, related_name = '+')
    father_first_language       = models.TextField ()
    father_accent               = models.TextField ()
    father_occupation           = models.TextField ()
    father_education_level      = models.TextField ()

    # Some other properties
    has_reading_problems        = models.BooleanField ()
    has_vocal_training          = models.BooleanField ()
    has_speech_problems         = models.BooleanField ()
    has_hearing_problems        = models.BooleanField ()
    is_left_handed              = models.BooleanField ()
    is_smoker                   = models.BooleanField ()
    has_dentures                = models.BooleanField ()
    has_piercings               = models.BooleanField ()
    has_health_problems         = models.BooleanField ()

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
        url_scheme = urlparse (self.identifier)
        (colour_id, animal_id) = re.findall ('\d+', url_scheme.path)
        return '%s_%s' % (colour_id, animal_id)


    def __unicode__ (self):
        """ Simple name representation for sites """
        
        url_scheme = urlparse (self.identifier)
        (colour_id, animal_id) = re.findall ('\d+', url_scheme.path)
        colour = Colour.objects.get (id = colour_id)
        animal = Animal.objects.get (id = animal_id)
        return '%s - %s (%s_%s)' % (colour.name, animal.name, colour_id, animal_id)


    class Meta:
        app_label= 'search'