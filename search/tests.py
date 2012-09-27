from django.utils import unittest
from search.models.sites import Sites
from search.models.sparql_local_wrapper import SparqlLocalWrapper

# Import SPARQL modules and related information
from search.settings import *
from SPARQLWrapper import SPARQLWrapper, JSON


class SiteTests (unittest.TestCase):

	def setUp (self):
		self.site1 = Sites.objects.create (name = "Australian National University", location = "Canberra")

	
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

