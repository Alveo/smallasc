from django.utils import unittest
from browse.modelspackage import *

# Import SPARQL modules and related information
from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlTests (unittest.TestCase):
    
    def test_site_prettyprinted_name (self):
        site1 = Site.objects.create (
            name = "Australian National University", 
            location = "Canberra",
            participant_count = 10)
        
        self.assertEqual ("Australian National University, Canberra", str (site1))


    def test_opendbpediasparql_endpoint (self):
       sparql = SPARQLWrapper ("http://dbpedia.org/sparql")
       sparql.setQuery ("""
           PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
           SELECT ?label
           WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
       """)

       sparql.setReturnFormat (JSON)
       results = sparql.query ().convert ()

       self.assertEqual (20, len (results["results"]["bindings"]))
           
    
class SiteTests (unittest.TestCase):

    def test_retrieveallsites (self):
        results = Site.objects.all ()
        
        # Assert that we are getting some data back and that the type of the objects returned
        # are what we expect
        self.assertTrue (len (results) > 0)
        self.assertTrue (results[0].participant_count > 0)

        self.assertTrue (isinstance (results[0], Site)) 


    def test_retrievenonexistingsite (self):
        self.assertIsNone (Site.objects.get ("BLAH"))


    def test_retrieveexistingsite (self):
        result = Site.objects.get ("UTAS")
        
        self.assertIsNotNone (result)
        self.assertTrue (isinstance (result, Site)) 
        self.assertEqual ("Hobart", result.location)


class SessionTests (unittest.TestCase):


    def test_retrieveallsessions (self):

        sessions = Session.objects.all ()
        
        # how many sessions in the store?
        self.assertTrue (len (sessions) > 0)
        self.assertTrue (isinstance (sessions[0], Session)) 


    def test_retrievespecificsession (self):
        sites = Site.objects.all ()
        parts = Participant.objects.all (sites[0])

        sessions = Session.objects.filter_by_participant (parts[0])

        """
        for s in sessions:
            print s.identifier
            print s.number
        """

        # how many sessions in the store?
        self.assertTrue (len (sessions) > 0)
        session = Session.objects.get (sessions[0].identifier)

        self.assertIsNotNone (session)
        self.assertTrue (isinstance (session, Session))
        self.assertEqual (session[0], session)


    def test_retrievecomponentsinsessions1 (self):
        sessions = Session.objects.all ()
        results = Component.objects.filter_by_session (sessions[0])

        self.assertTrue (len (results) > 0)
        self.assertEqual ('Calibration', str (results[0]))

    
    def test_retrievesessioncomponents (self):
        sessions = Session.objects.all ()
        components = Component.objects.filter_by_session (sessions[0])
        
        self.assertTrue (len (components) > 0)


class ParticipantTests (unittest.TestCase):

    def test_retrieveparticipantsforexistingsite (self):
        sites = Site.objects.all ()
        parts = Participant.objects.all (sites[0])

        self.assertTrue (len (parts) > 0)
        self.assertTrue (isinstance (parts[0], Participant)) 


    def test_retrievespecificparticipant (self):
        sites = Site.objects.all ()
        parts = Participant.objects.all (sites[0])

        self.assertTrue (len(parts) > 0)

        part = Participant.objects.get (parts[0].friendly_id ())
        
        self.assertIsNotNone(part)
        self.assertTrue (isinstance (part, Participant)) 
        self.assertEqual (parts[0].identifier, part.identifier)
        self.assertEqual (parts[0].friendly_id (), part.friendly_id ())


    def test_retrievesessionbyparticipant (self):
        sites = Site.objects.all ()
        parts = Participant.objects.all (sites[0])
        sessions = Session.objects.filter_by_participant (parts[0])

        self.assertTrue (len (sessions) > 0)


    def test_retrieveeducationbyparticipant (self):
        sites = Site.objects.all ()
        parts = Participant.objects.all (sites[0])

        eh = EducationHistory.objects.filter_by_participant (parts[0])

        self.assertIsNotNone (eh)
        self.assertTrue (len (eh) > 0)


    def test_retrieveprofessionbyparticipant (self):
        sites = Site.objects.all ()
        parts = Participant.objects.all (sites[0])
       
        ph = ProfessionalHistory.objects.filter_by_participant (parts[1])
        
        self.assertIsNotNone (ph)
        self.assertTrue (len (ph) > 0)
        self.assertIsNotNone (ph[0].name)


    def test_checkmothersdetailspresent (self):
        sites = Site.objects.all ()
        parts = Participant.objects.all (sites[0])

        self.assertTrue (len(parts) > 0)
        self.assertTrue (isinstance (parts[0], Participant)) 
        self.assertIsNotNone (parts[0].mother_first_language)


    def test_retrieveitemproperties (self):
        
        items = Item.objects.filter_by_component("1_1093", "1", "words-1")
        
        self.assertTrue (len(items) > 0)
        item = items[0]
        props = item.properties()
        self.assertEqual(props['bar'], 'foo')


    def test_retrievemedia (self): 
        items = Item.objects.filter_by_component("1_1093", "2", "sentences")
        self.assertEqual (59, len (items))
        media = Media.filter_by_componentitems (components[0], items[0])


    def test_filterwithnopredicates(self):

        participants = Participant.objects.filter()
        self.assertTrue(len(participants) > 0)
        
        #for part in participants:
        #    print part.properties()
        #    print part.friendly_id()


    def test_filterbygender (self):
        predicates = {  
            "foaf:gender": "male", 
            "austalk:ses": "Professional", 
            "austalk:education_level": "Bachelor Degree", 
            "austalk:professional_category": "assoc professional"
        }

        male_qual_parts = Participant.objects.filter (predicates)
        
        self.assertTrue (len (male_qual_parts) > 0)

        predicates = {  
            "foaf:gender": "male",
            "austalk:ses": "Professional",
            "austalk:education_level": "Bachelor Degree"
        }
        male_parts = Participant.objects.filter (predicates)

        self.assertTrue (len (male_parts) > 0)
        self.assertTrue (len (set (male_qual_parts).intersection (set (male_parts))) == len (male_qual_parts))


class ComponentTests (unittest.TestCase):

    def test_filterbyparticipant (self):
        components = Component.objects.filter_by_participant ("2_566")
        self.assertTrue (len (components) > 0)

        for comp in components:
            print "%s - %s" % (comp.sessionId, comp.name)


class ItemTests (unittest.TestCase):

    def test_filterbyparticipant (self):
        items = Item.objects.filter_by_participant ("2_566")
        self.assertTrue (len (items) > 0)
