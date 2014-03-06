from django import forms
from django.forms.widgets import CheckboxSelectMultiple

# Models in use
from browse.modelspackage import Site

# this could be generated from a query but to save time it's hard-coded here
COMPONENT_CHOICES = (
                     ('calibration', 'calibration'),
                     ('yes-no-opening-1', 'yes-no-opening-1'),
                     ('yes-no-opening-2', 'yes-no-opening-2'),
                     ('yes-no-opening-3', 'yes-no-opening-3'),
                     ('yes-no-closing', 'yes-no-closing'),
                     ('story', 'story'),
                     ('re-told-story', 're-told-story'),
                     ('digits', 'digits'),
                     ('sentences', 'sentences'),
                     ('interview', 'interview'),
                     ('maptask-1', 'maptask-1'),
                     ('maptask-2', 'maptask-2'),
                     ('conversation', 'conversation'),
                     ('sentences', 'sentences'),
                     ('sentences-e', 'sentences-e'),
                     ('words-1', 'words-1'),
                     ('words-2', 'words-2'),
                     ('words-3', 'words-3'),
                     ('words-2-2', 'words-2-2'),
                     ('words-3-2', 'words-3-2'),
                     ('words-1-2', 'words-1-2'),
                     )


QA_AUDIO_CHOICES = (('any', 'Any'),
                    ('A', 'A'),
                    ('B', 'B'),
                    ('C', 'C'),
                    ('D', 'D'))

class PromptSearchForm (forms.Form):
    """ Form used to represent the composite search fields """
    # Construct the sites choice list in the form

    prompt = forms.CharField(label='Prompts separated by comma') 
    
   # components = forms.MultipleChoiceField(widget     = CheckboxSelectMultiple (),
   #                                        label       = 'Components',
   #                                        required    = False,
   #                                        choices     = COMPONENT_CHOICES)
    
   # qa_audio = forms.ChoiceField(label="Audio Quality", 
    #                             choices=QA_AUDIO_CHOICES)
    
    
    
    
    