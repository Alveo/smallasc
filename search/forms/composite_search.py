from django import forms
from django.forms.widgets import CheckboxSelectMultiple

# Models in use
from browse.modelspackage import Site
from browse.modelspackage import Protocol

def component_choices():

    p = Protocol()
    
    return p.components() 

class CompositeSearchForm (forms.Form):
    """ Form used to represent the composite search fields """
    # Construct the sites choice list in the form

    prompt = forms.CharField(label='Prompt contains')
    wholeword = forms.BooleanField(label="Match whole word", required=False)
    components = forms.MultipleChoiceField(widget     = CheckboxSelectMultiple (),
                                           label       = 'Components',
                                           required    = False,
                                           choices     = component_choices())