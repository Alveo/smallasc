# Import SPARQL modules and related information
from search.settings import *
from SPARQLWrapper import SPARQLWrapper, JSON

class SparqlLocalWrapper ():

    @staticmethod
    def canonicalise_query (query):
        """ Each query needs to be preceeded with the namespaces used for the query, this method
        returns all such namespaces. """
        namespaces =   """PREFIX dc:<http://purl.org/dc/terms/>
                        PREFIX austalk:<http://ns.austalk.edu.au/>
                        PREFIX olac:<http://www.language-archives.org/OLAC/1.1/>
                        PREFIX ausnc:<http://ns.ausnc.org.au/schemas/ausnc_md_model/>
                        PREFIX foaf:<http://xmlns.com/foaf/0.1/>
                        PREFIX dbpedia:<http://dbpedia.org/ontology/>
                        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX ns1:<http://purl.org/dc/terms/>
                        %s"""
        return namespaces % query

    @staticmethod
    def create_sparql ():
        """ This function creates a wrapper class used to communicate with the SPARQL endpoint """
        sparql = SPARQLWrapper (SPARQL_ENDPOINT)
        sparql.setReturnFormat (JSON)
        return sparql