from django.db import models
from browse.modelspackage.sparql_local_wrapper import SparqlLocalWrapper


class Location (models.Model):
    """ A session is a logical representation of the actual recording session
    which takes place at a particular location."""

    # Note that id is not specified as this is a Django model
    country = models.TextField ()
    state   = models.TextField ()
    town    = models.TextField ()


    def __unicode__ (self):
        """ Simple name representation for a session """
        return "%s %s, %s" % (self.town, self.state, self.country)


    class Meta:
        app_label = 'search'