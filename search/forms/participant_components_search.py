from django import forms

from search.forms                       import ParticipantSearchFilterForm
from search.forms.choice_options        import *


class ParticipantComponentSearchForm(ParticipantSearchFilterForm):


    components_field    = forms.MultipleChoiceField (
        widget          = forms.CheckboxSelectMultiple,
        error_messages  = { 'required': 'Please select from the following list of components'},
        label           = "Components")


    def __init__(self, participants, components, *args, **kwargs):

        super(ParticipantComponentSearchForm, self).__init__(participants, *args, **kwargs)

        self.fields["participants_field"].required  = False
        self.fields["participants_field"].widget    = forms.MultipleHiddenInput()

        if not components is None:
            self.components                         = components
            self.fields["components_field"].choices = EXTRA_CHOICES
            self.fields["components_field"].choices.extend([(comp.identifier, "Session %s - Component %s" % (comp.sessionId, comp)) for comp in components])


    def return_selected_components(self):

        results = []

        if u'all' in self.cleaned_data["components_field"]:

            results = self.components
        
        else:

            for component in self.components:
                if component.identifier in self.cleaned_data["components_field"]:
                    results.append(component)

            
        return results