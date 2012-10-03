from django import forms
from django.forms.widgets import CheckboxSelectMultiple

# Models in use
from search.models.sites import Sites
from search.models.sessions import Sessions
from search.models.sparql_local_wrapper import SparqlLocalWrapper

class CompositeSearchForm (forms.Form):
    """ Form used to represent the composite search fields """
    # Construct the sites choice list in the form
    sites = Sites.all (SparqlLocalWrapper.create_sparql ())
    site_choices = [(site.site, str (site)) for site in sites]
    sites_field = forms.MultipleChoiceField(widget=CheckboxSelectMultiple (),
                                            label = 'Recording Locations',
                                            required = True, 
                                            choices = site_choices)

    # Construct the sessions choice list in the form
    sessions = Sessions.all (SparqlLocalWrapper.create_sparql ())
    session_choices = [(session.id, session.name) for session in sessions]
    sessions_field = forms.MultipleChoiceField(widget=CheckboxSelectMultiple (),
                                                label = 'Sessions',
                                                required = True, 
                                                choices = session_choices)
