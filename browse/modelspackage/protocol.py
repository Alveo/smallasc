from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlMixin



class Protocol(SparqlMixin):
    """A class to access information about the collection protocol"""
        
    def sessions(self):
        """Return a list of all sessions with their names
        [(<http://id.austalk.edu.au/protocol/1>, 'Session 1') ...]
        """
        
        q = """
        SELECT ?id ?name WHERE
        {
         ?id a austalk:Session .
         ?id austalk:name ?name .
        }
        ORDER BY ?name
        """
        
        sparql_results = self.query(q)

        result = []
        for row in sparql_results["results"]["bindings"]:
            result.append((row["id"]["value"], row["name"]["value"]))
            
        return result
    
    
    def components(self, sessionid=None):
        """Return a list of all components with their names
        [(words-1, 'Words Session 1') ...]
        
        if sessionid is provided, list only components in that session
        """
        
        q = """
        SELECT ?shortname ?name WHERE
        {
         ?id a austalk:Component .
         ?id austalk:shortname ?shortname .
         ?id austalk:name ?name .
        }
        ORDER BY ?name
        """
        
        sparql_results = self.query(q)

        result = []
        for row in sparql_results["results"]["bindings"]:
            result.append((row["shortname"]["value"], row["name"]["value"] + " (" + row["shortname"]["value"] + ")"))
            
        return result