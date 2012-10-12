from django.db import models
from search.modelspackage.sparql_local_wrapper import SparqlLocalWrapper, SparqlModel, SparqlManager

class ItemManager (SparqlManager):
    """Manager for items implements operations returning lists of Item instances"""
    
    def filter_by_component (self, participant_id, session_id, component_id):
        """ Method returns all the items filtered by the participant/session/component. """
        
        qq = """
            select ?item ?id ?prompt ?basename ?sitelabel ?media
            where {
                ?rc rdf:type austalk:RecordedComponent .
                ?rc olac:speaker <http://id.austalk.edu.au/participant/%(part)s> .
                <http://id.austalk.edu.au/participant/%(part)s> austalk:recording_site ?site .
                ?site rdfs:label ?sitelabel .
                ?rc austalk:prototype ?component .
                ?rc dc:isPartOf ?rs .
                 ?rs austalk:prototype ?session .
                ?session austalk:id %(sess)s .
                ?component austalk:shortname "%(comp)s" .
                ?item dc:isPartOf ?rc .
                ?item austalk:prototype ?ip .
                ?item austalk:basename ?basename .
                ?ip austalk:id ?id .
                ?ip austalk:prompt ?prompt .
                ?item austalk:media ?media .
                ?media austalk:version 1 .
                ?media austalk:channel "ch6-speaker" .
        } order by ?id""" % {'part': participant_id, 'sess': session_id, 'comp': component_id}
     
        print qq
     
        sparql_results = self.query (qq)
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Item (
                                identifier      = result["item"]["value"], 
                                id              = result["id"]["value"], 
                                prompt          = result["prompt"]["value"],
                                basename        = result["basename"]["value"],
                                site            = result["sitelabel"]["value"],
                                participantId   = participant_id,
                                componentId     = component_id,
                                sessionId       = session_id,
                                ch6media        = result["media"]["value"]
                                ))

        return results
   
    def get (self, basename):
        """ Return the item with this basename. """
        
        qq = """
            select ?item ?id ?prompt ?basename ?sitelabel ?spkrid ?sessid ?compid ?media
            where {
                ?item austalk:basename "%s" .
                ?item dc:isPartOf ?rc .
                ?item austalk:prototype ?ip .
                ?ip austalk:id ?id .
                ?ip austalk:prompt ?prompt .
                ?rc rdf:type austalk:RecordedComponent .
                ?rc olac:speaker ?spkr .
                ?spkr austalk:id ?spkrid .
                ?spkr austalk:recording_site ?site .
                ?site rdfs:label ?sitelabel .
                ?rc austalk:prototype ?component .
                ?component dc:isPartOf ?session .
                ?session austalk:id ?sessid .
                ?component austalk:shortname ?compid  .
                ?item austalk:media ?media .
                ?media austalk:version 1 .
                ?media austalk:channel "ch6-speaker" .
        } order by ?id""" % (basename, )
     
        print qq
     
        sparql_results = self.query (qq)
        results = []

        for result in sparql_results["results"]["bindings"]:
            return Item (
                                identifier      = result["item"]["value"], 
                                id              = result["id"]["value"], 
                                prompt          = result["prompt"]["value"],
                                basename        = basename,
                                site            = result["sitelabel"]["value"],
                                participantId   = result["spkrid"]["value"],
                                componentId     = result["compid"]["value"],
                                sessionId       = result["sessid"]["value"],
                                ch6media        = result["media"]["value"]
                                )
        # Item not found
        return None
 
 
class Item (SparqlModel):
    """ A item is a logical representation of an item which belongs
    to a component."""

    # Note that id is not specified as this is a Django model
    # identifier field is inherited from SparqlModel
    prompt = models.TextField ()
    basename = models.TextField ()
    participantId = models.TextField ()
    componentId = models.TextField ()
    sessionId = models.TextField ()
    site = models.TextField ()
    ch6media = models.URLField ()  
    
    # a custom manager
    objects = ItemManager ()     
        
    def get_absolute_url(self):
        """Return a canonical URL for this item"""
                
        return "/browse/%s/%s/%s/%s/%s" % (self.site, self.participantId, self.sessionId, self.componentId, self.basename)    

    
        
        
        
    class Meta:
        app_label= 'search'