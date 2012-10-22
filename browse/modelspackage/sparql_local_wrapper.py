# Import SPARQL modules and related information
from browse.settings import *
from SPARQLWrapper import SPARQLWrapper, JSON
import os

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
    
from django.db import models

class SparqlMixin(object):
    """Mixin class to implement a query method. 
    Intended for use in both SparqlManager and SparqlModel but I can't
    work out how to make that work with metaclasses and all
    so for now, the code is repeated below"""
    
    def __init__(self):
        self.create_sparql()

    def canonicalise_query (self, query):
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

    def create_sparql (self):
        """ This function creates a wrapper class used to communicate with the SPARQL endpoint """
        self.sparql = SPARQLWrapper (SPARQL_ENDPOINT)
        self.sparql.setReturnFormat (JSON)
        
    def query(self, query):
        """Run a SPARQL query, first add the required PREFIX 
        definitions to the start of the query. Return
        a Python dictionary that reflects the JSON returned
        from the SPARQL endpoint"""
        
        self.sparql.setQuery(self.canonicalise_query(query))
        return self.sparql.query().convert()


class SparqlManager(models.Manager):
    """Manager class for sparql models"""

    def __init__(self, *args, **kwargs):
         
        super(SparqlManager, self).__init__(*args, **kwargs)
 

        self.create_sparql()
        
    
    def canonicalise_query (self, query):
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

    def create_sparql (self):
        """ This function creates a wrapper class used to communicate with the SPARQL endpoint """
        self.sparql = SPARQLWrapper (SPARQL_ENDPOINT)
        self.sparql.setReturnFormat (JSON)
        
    def query(self, query):
        """Run a SPARQL query, first add the required PREFIX 
        definitions to the start of the query. Return
        a Python dictionary that reflects the JSON returned
        from the SPARQL endpoint"""
        
        self.sparql.setQuery(self.canonicalise_query(query))
        return self.sparql.query().convert()



class SparqlModel(models.Model):
    
    # all sparql models have an identifier that is their URI in the triple store
    identifier      = models.URLField ()
    
    def __init__(self, *args, **kwargs):
            
        super(SparqlModel, self).__init__(*args, **kwargs)
        
        self.props = None
        self.create_sparql()


    def canonicalise_query (self, query):
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

    def create_sparql (self):
        """ This function creates a wrapper class used to communicate with the SPARQL endpoint """
        self.sparql = SPARQLWrapper (SPARQL_ENDPOINT)
        self.sparql.setReturnFormat (JSON)
    
    def query(self, query):
        """Run a SPARQL query, first add the required PREFIX 
        definitions to the start of the query. Return
        a Python dictionary that reflects the JSON returned
        from the SPARQL endpoint"""
        
        self.sparql.setQuery(self.canonicalise_query(query))
        return self.sparql.query().convert()

    def clean_property_name(self, prop):
        """Generate a 'nice' version of the property name 
        which is an RDF URI"""
        
        if prop.startswith('http'):
            return os.path.basename(prop)
        else:
            return prop
        
    
    def properties(self):
        """Return a dictionary of properties for this object
        each property value is a list to allow for multiple
        values"""
        
        if self.props != None:
            return self.props
        
        
        qq = """
            select ?prop ?value
            where {
                <%s> ?prop ?value .
        }""" % self.identifier
        
        sparql_results = self.query (qq)
        self.props = dict()

        for result in sparql_results["results"]["bindings"]:
            prop = self.clean_property_name(result["prop"]["value"])
            value = result["value"]["value"]
            
            if self.props.has_key(prop):
                self.props[prop].append(value)
            else:
                self.props[prop] = [value]
        
        return self.props
    
    
    class Meta:
        abstract = True
        
        
        