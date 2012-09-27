# Import SPARQL modules and related information
from search.settings import *
from SPARQLWrapper import SPARQLWrapper, JSON

class SparqlLocalWrapper():

    @staticmethod
    def create_sparql ():
        sparql = SPARQLWrapper (SPARQL_ENDPOINT)
        sparql.setReturnFormat (JSON)
        return sparql