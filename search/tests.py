from django.utils import unittest
from search.models.sites import Sites
from search.models.sessions import Sessions
from search.models.components import Components
from search.models.participants import Participants
from search.models.sparql_local_wrapper import SparqlLocalWrapper

# Import SPARQL modules and related information
from search.settings import *
from SPARQLWrapper import SPARQLWrapper, JSON


class SiteTests (unittest.TestCase):


	def setUp (self):
		self.site1 = Sites.objects.create (name = "Australian National University", 
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
		results = Sites.all (SparqlLocalWrapper.create_sparql ())
		self.assertEqual (10, len (results))
		self.assertEqual ('Charles Sturt University, Bathurst', str (results[0]))
		self.assertEqual (47, results[0].participant_count)


	def test_retrievenonexistingsite (self):
		self.assertIsNone (Sites.get (SparqlLocalWrapper.create_sparql (), "BLAH"))


	def test_retrievenonexistingsite (self):
		site = Sites.get (SparqlLocalWrapper.create_sparql (), "CSUB")
		self.assertIsNotNone (site)
		self.assertEqual ("Bathurst", site.location)


	def test_retrieveallsessions (self):
		results = Sessions.all (SparqlLocalWrapper.create_sparql ())
		self.assertEqual (4, len (results))
		self.assertEqual ('Session 1', str (results[0]))


	def test_retrievecomponentsinsessions1and2 (self):
		results = Components.all (SparqlLocalWrapper.create_sparql ())
		self.assertEqual (13, len (results))
		self.assertEqual ('Calibration', str (results[0]))


	def test_retrieveparticipantsforexistingsite (self):
		sites = Sites.all (SparqlLocalWrapper.create_sparql ())
		parts = Participants.all ((SparqlLocalWrapper.create_sparql ()), sites[0])
		self.assertEqual (47, len (parts))

