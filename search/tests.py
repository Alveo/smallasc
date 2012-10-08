from django.utils import unittest
from search.models import *

# Import SPARQL modules and related information
from search.settings import *
from SPARQLWrapper import SPARQLWrapper, JSON


class SiteTests (unittest.TestCase):

	def setUp (self):
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
		results = Site.all (SparqlLocalWrapper.create_sparql ())
		self.assertEqual (10, len (results))
		self.assertEqual ('Charles Sturt University, Bathurst', str (results[0]))
		self.assertEqual (47, results[0].participant_count)


	def test_retrievenonexistingsite (self):
		self.assertIsNone (Site.get (SparqlLocalWrapper.create_sparql (), "BLAH"))


	def test_retrievenonexistingsite (self):
		site = Site.get (SparqlLocalWrapper.create_sparql (), "CSUB")
		self.assertIsNotNone (site)
		self.assertEqual ("Bathurst", site.location)


	def test_retrieveallsessions (self):
		results = Session.all (SparqlLocalWrapper.create_sparql ())
		self.assertEqual (4, len (results))
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
		part = Participant.get (SparqlLocalWrapper.create_sparql (), "1_978")
		self.assertIsNotNone(part)
		self.assertEqual ("female", part.gender)


	def test_retrievesessionbyparticipant (self):
		part = Participant.get (SparqlLocalWrapper.create_sparql (), "1_978")
		sess = Session.filter_by_participant (SparqlLocalWrapper.create_sparql (), part)
		self.assertIsNotNone (sess)
		self.assertEqual (4, len (sess))


	def test_retrieveeducationbyparticipant (self):
		part = Participant.get (SparqlLocalWrapper.create_sparql (), "1_978")
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
