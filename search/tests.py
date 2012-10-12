from django.utils import unittest
from search.modelspackage import *

# Import SPARQL modules and related information
from search.settings import *
from SPARQLWrapper import SPARQLWrapper, JSON

class SiteTests (unittest.TestCase):

    def setUp (self):
        self.site_man = SiteManager ()
        self.site1 = Site.objects.create (name = "Australian National University", 
                                           location = "Canberra",
                                           participant_count = 10)
    

    def test_site_prettyprinted_name (self):
        self.assertEqual ("Australian National University, Canberra", str (self.site1))
    

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
        self.assertEqual (10, len (results))
        self.assertEqual ('Charles Sturt University, Bathurst', str (results[0]))
        self.assertEqual (47, results[0].participant_count)


    def test_retrievenonexistingsite (self):
        self.assertIsNone (self.site_man.get ("BLAH"))


    def test_retrieveexistingsite (self):
        result = self.site_man.get ("CSUB")
        self.assertIsNotNone (result)
        self.assertEqual ("Bathurst", result.location)


    def test_retrieveallsessions (self):
        results = Session.all (SparqlLocalWrapper.create_sparql ())
        # how many sessions in the store?
        self.assertEqual (18, len (results))
        self.assertEqual ('Session 1', str (results[0]))


    def test_retrievecomponentsinsessions1and2 (self):
        results = Component.all (SparqlLocalWrapper.create_sparql ())
        self.assertEqual (13, len (results))
        self.assertEqual ('Calibration', str (results[0]))


    def test_retrieveparticipantsforexistingsite (self):
        sites = Site.all (SparqlLocalWrapper.create_sparql ())
        parts = Participant.all ((SparqlLocalWrapper.create_sparql ()), sites[0])
        self.assertEqual (47, len (parts))


    def test_retrievespecificparticipant (self):
        part = Participant.get (SparqlLocalWrapper.create_sparql (), "1_1093")
        self.assertIsNotNone(part)
        self.assertEqual ("female", part.gender)


    def test_retrievesessionbyparticipant (self):
        part = Participant.get (SparqlLocalWrapper.create_sparql (), "1_1093")
        sess = Session.filter_by_participant (SparqlLocalWrapper.create_sparql (), part)
        self.assertIsNotNone (sess)
        self.assertEqual (4, len (sess))


    def test_retrieveeducationbyparticipant (self):
        part = Participant.get (SparqlLocalWrapper.create_sparql (), "1_1093")
        eh = EducationHistory.filter_by_participant (SparqlLocalWrapper.create_sparql (), part)
        self.assertIsNotNone (eh)
        self.assertEqual (3, len (eh))


    def test_retrieveeducationbyparticipant (self):
        part = Participant.get (SparqlLocalWrapper.create_sparql (), "1_978")
        ph = ProfessionalHistory.filter_by_participant (SparqlLocalWrapper.create_sparql (), part)
        self.assertIsNotNone (ph)
        self.assertEqual (1, len (ph))
        self.assertEqual ("Teaching K-12", ph[0].name)


    def test_checkmothersdetailspresent (self):
        part = Participant.get (SparqlLocalWrapper.create_sparql (), "1_978")
        self.assertIsNotNone (part)
        self.assertEqual ("English", part.mother_first_language)


    def test_retrievesessioncomponents (self):
        sessions = Session.all (SparqlLocalWrapper.create_sparql ())
        components = Component.filter_by_session (SparqlLocalWrapper.create_sparql (), sessions[0])
        self.assertEqual (7, len (components))


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
