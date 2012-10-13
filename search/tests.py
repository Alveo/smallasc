from django.utils import unittest
from search.modelspackage import *

# Import SPARQL modules and related information
from search.settings import *
from SPARQLWrapper import SPARQLWrapper, JSON

class SiteTests (unittest.TestCase):


    def setUp (self):
        self.site_man = SiteManager ()
        self.part_man = ParticipantManager ()
        self.sess_man = SessionManager ()
        self.comp_man = ComponentManager ()
        self.profhist_man = ProfessionalHistoryManager ()
        self.edhist_man = EducationHistoryManager ()


    def test_site_prettyprinted_name (self):
        site1 = Site.objects.create (name = "Australian National University", 
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


    def test_retrieveallsites (self):
        results = self.site_man.all ()
        
        # Assert that we are getting some data back and that the type of the objects returned
        # are what we expect
        self.assertTrue (len (results) > 0)
        self.assertTrue (results[0].participant_count > 0)

        self.assertTrue (isinstance (results[0], Site)) 


    def test_retrievenonexistingsite (self):
        self.assertIsNone (self.site_man.get ("BLAH"))


    def test_retrieveexistingsite (self):
        result = self.site_man.get ("UTAS")
        
        self.assertIsNotNone (result)
        self.assertTrue (isinstance (result, Site)) 
        self.assertEqual ("Hobart", result.location)


    def test_retrieveallsessions (self):
        sessions = self.sess_man.all ()
        
        # how many sessions in the store?
        self.assertTrue (len (sessions) > 0)
        self.assertTrue (isinstance (sessions[0], Session)) 


    def test_retrievespecificsession (self):
        sites = self.site_man.all ()

        self.assertTrue (len (sites) > 0)
        parts = self.part_man.all (sites[0])

        self.assertTrue (len (parts) > 0)
        sessions = self.sess_man.filter_by_participant (parts[0])

        # how many sessions in the store?
        self.assertTrue (len (sessions) > 0)
        session = self.sess_man.get (sessions[0].identifier)

        self.assertIsNotNone (session)
        self.assertTrue (isinstance (session, Session))
        self.assertEqual (session[0], session)


    def test_retrievecomponentsinsessions1 (self):
        sessions = self.sess_man.all ()
        results = self.comp_man.filter_by_session (sessions[0])

        self.assertTrue (len (results) > 0)
        self.assertEqual ('Calibration', str (results[0]))


    def test_retrieveparticipantsforexistingsite (self):
        sites = self.site_man.all ()
        parts = self.part_man.all (sites[0])

        self.assertTrue (len (parts) > 0)
        self.assertTrue (isinstance (parts[0], Participant)) 


    def test_retrievespecificparticipant (self):
        sites = self.site_man.all ()
        parts = self.part_man.all (sites[0])

        self.assertTrue (len(parts) > 0)

        part = self.part_man.get (parts[0].friendly_id ())
        
        self.assertIsNotNone(part)
        self.assertTrue (isinstance (part, Participant)) 
        self.assertEqual (parts[0].identifier, part.identifier)
        self.assertEqual (parts[0].friendly_id (), part.friendly_id ())


    def test_retrievesessionbyparticipant (self):
        sites = self.site_man.all ()
        parts = self.part_man.all (sites[0])
        sessions = self.sess_man.filter_by_participant (parts[0])

        self.assertTrue (len (sessions) > 0)


    def test_retrieveeducationbyparticipant (self):
        sites = self.site_man.all ()
        parts = self.part_man.all (sites[0])

        eh = self.edhist_man.filter_by_participant (parts[0])

        self.assertIsNotNone (eh)
        self.assertTrue (len (eh) > 0)


    def test_retrieveprofessionbyparticipant (self):
        sites = self.site_man.all ()
        parts = self.part_man.all (sites[0])
       
        ph = self.profhist_man.filter_by_participant (parts[1])
        
        self.assertIsNotNone (ph)
        self.assertTrue (len (ph) > 0)
        self.assertIsNotNone (ph[0].name)


    def test_checkmothersdetailspresent (self):
        sites = self.site_man.all ()
        parts = self.part_man.all (sites[0])

        self.assertTrue (len(parts) > 0)
        self.assertTrue (isinstance (parts[0], Participant)) 
        self.assertIsNotNone (parts[0].mother_first_language)


    def test_retrievesessioncomponents (self):
        sessions = self.sess_man.all ()
        components = self.comp_man.filter_by_session (sessions[0])
        
        self.assertTrue (len (components) > 0)


    def test_retrieveitemproperties (self):
        
        items = Item.filter_by_component(SparqlLocalWrapper.create_sparql (), "1_1093", "1", "words-1")
        self.assertEqual(323, len(items))
        item = items[0]
        print "IDENT: ", item.identifier
        props = item.properties(SparqlLocalWrapper.create_sparql ())
        print "PROPS: ", props
        self.assertEqual(props['bar'], 'foo')



    def test_retrievemedia (self): 
        
        items = Item.filter_by_component(SparqlLocalWrapper.create_sparql (), "1_1093", "2", "sentences")

        # There should be 59 items for sentences
        self.assertEqual (59, len (items))
        print items
        # Now get the media
        media = Media.filter_by_componentitems (SparqlLocalWrapper.create_sparql (), components[0], items[0])

        print components[0].identifier
        print items[0].identifier
