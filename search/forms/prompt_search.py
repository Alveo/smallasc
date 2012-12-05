from django import forms
from django.forms.widgets import CheckboxSelectMultiple

# Models in use
from browse.modelspackage import Site
from browse.modelspackage import Protocol

def component_choices():

    p = Protocol()
    
    return p.components() 

QA_AUDIO_CHOICES = (('any', 'Any'),
                    ('A', 'A'),
                    ('B', 'B'),
                    ('C', 'C'),
                    ('D', 'D'))

class PromptSearchForm (forms.Form):
    """ Form used to represent the composite search fields """
    # Construct the sites choice list in the form

    prompt = forms.CharField(label='Prompt contains')
    wholeword = forms.BooleanField(label="Match whole word", required=False)

    
class ComponentSearchForm(forms.Form):
    """Form to select items by component """
    
    components = forms.MultipleChoiceField(widget     = CheckboxSelectMultiple (),
                                           label       = 'Components',
                                           required    = False,
                                           choices     = component_choices())
    
    qa_audio = forms.Choicefield(label="Audio Quality", 
                                 choices=QA_AUDIO_CHOICES)