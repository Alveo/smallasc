from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlModel, SparqlManager

class ItemManager (SparqlManager):
    """Manager for items implements operations returning lists of Item instances"""

    def generate_list(self, qpart):

        qq = """
            select distinct ?item ?prompt ?basename ?sitelabel ?media ?spkrname ?sessid ?compid
            where {

                %s

                ?item olac:speaker ?spkrid .
                ?spkrid austalk:recording_site ?site .
                ?spkrid austalk:id ?spkrname .
                ?site rdfs:label ?sitelabel .

                ?item austalk:session ?sessid .
                ?item austalk:componentName ?compid .
                ?item dc:title ?basename .
                ?item  austalk:prototype ?prot .
                ?prot austalk:prompt ?prompt .
                ?item ausnc:document ?media .
                ?media austalk:version 1 .
                ?media austalk:channel "ch6-speaker16" .

        } order by ?basename""" % (qpart,)

        sparql_results = self.query (qq)
        results = []

        for result in sparql_results["results"]["bindings"]:
            results.append (Item (
                                client            = self.client,
                                identifier      = result["item"]["value"],
                                prompt          = result["prompt"]["value"],
                                basename        = result["basename"]["value"],
                                site            = result["sitelabel"]["value"],
                                participantId   = result["spkrname"]["value"],
                                componentId     = result["compid"]["value"],
                                sessionId       = result["sessid"]["value"],
                                ch6media        = result["media"]["value"]
                                ))

        return results


    def filter_by_component (self, participant_id, session_id, component_id):
        """ Method returns all the items filtered by the participant/session/component. """

        qq = """
                BIND (<https://app.alveo.edu.au/speakers/austalk/%(part)s> as ?spkrid)
                BIND ("%(sess)s" as ?sessid)
                BIND ("%(comp)s" as ?compid)
            """ % {'part': participant_id, 'sess': session_id, 'comp': component_id}

        return self.generate_list(qq)


    def get (self, participant_id, basename):
        """ Return the item for this participant with this basename. """

        qq = """BIND ("%s" as ?basename)
        BIND (<https://app.alveo.edu.au/speakers/austalk/%s> as ?spkrid)""" % (basename, participant_id)

        result = self.generate_list(qq)

        if result != None:
            return result[0]
        else:
            return None


    def filter_by_participant (self, participant_id):
        qq = """BIND (<https://app.alveo.edu.au/speakers/austalk/%s> as ?spkrid)""" % (participant_id)
        return self.generate_list (qq)


    def filter_by_prompt (self, prompt, components, wholeword=False):
        """Search through items in components, returning all
        those that contain the text in prompt"""

        if wholeword:
            qpart = 'BIND ("%s" as ?prompt)' % (prompt,)
        else:
            qpart = 'FILTER (regex(?prompt, "%s"))' % (prompt, )

        items = self.generate_list(qpart)

        # filter by components if we have any, passing none implies
        # that we take all components
        if components != []:
            items = [i for i in items if i.componentId in components]

        return items

    def filter_by_prompts(self, prompts):
        """Return a list of items with one of the given prompts
        Faster search optimised for prompt search page."""

        union = ['{?prot austalk:prompt "%s"}' % p for p in prompts]
        union = " UNION ".join(union)

        qq = """
            select distinct ?item ?prompt ?basename ?compid ?uni
            where {

                ?item austalk:session ?sessid .
                ?item austalk:componentName ?compid .
                ?item dc:title ?basename .
                ?item  austalk:prototype ?prot .
                ?prot austalk:prompt ?prompt .
                
                ?item olac:speaker ?speaker .
                ?speaker austalk:recording_site ?site .
                ?site rdfs:label ?uni

                %s .

        } order by ?basename""" % (union,)

        sparql_results = self.query (qq)
        results = []

        for result in sparql_results["results"]["bindings"]:
            parts = result["item"]["value"].split('/')[-1].split('_')
            results.append (Item (
                                client            = self.client,
                                identifier      = result["item"]["value"],
                                prompt          = result["prompt"]["value"],
                                basename        = result["basename"]["value"],
                                componentId          = result["compid"]["value"],
                                site          = result["uni"]["value"],
                                participantId = "%s_%s" % (parts[0],parts[1]),
                                sessionId = parts[2]
                                ))

        return results



class Item (SparqlModel):
    """ A item is a logical representation of an item which belongs
    to a component."""

    # custom manager
    objects = ItemManager ()

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

        return "/browse/%s/%s/%s/%s/%s" % (self.site,
            self.participantId, self.sessionId, self.componentId, self.basename)


    class Meta:
        app_label= 'search'
