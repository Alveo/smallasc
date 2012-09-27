from django import forms
from django.forms.widgets import CheckboxSelectMultiple

# Models in use
from search.models.sites import Sites
from search.models.sparql_local_wrapper import SparqlLocalWrapper


class CompositeSearchForm (forms.Form):
    """ Form used to represent the composite search fields """
    sites = Sites.all (SparqlLocalWrapper.create_sparql ())
    choices = [(site.site, str (site)) for site in sites]
    sites_field = forms.MultipleChoiceField(widget=CheckboxSelectMultiple (),
                                                label = 'Recording Locations',
                                                required = True, 
                                                choices = choices)