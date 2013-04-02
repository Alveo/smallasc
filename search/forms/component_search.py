from django                             import forms
from django.core.validators             import MaxValueValidator, MinValueValidator

from search.forms                       import ParticipantSearchForm
from search.forms.choice_options        import *


class ComponentSearchForm(ParticipantSearchForm):

    DEFAULT_SPEAKER_QUANTITY = 1

    components_field    = forms.MultipleChoiceField (
        widget          = forms.CheckboxSelectMultiple,
        error_messages  = { 'required': 'Please select from the following list of components'},
        label           = "Components"
    )

    speaker_no_field    = forms.IntegerField(
        widget          = forms.TextInput(attrs = {'value' : DEFAULT_SPEAKER_QUANTITY}),
        error_messages  = { 'required': 'Please provide a number between 1 and 100'},
        min_value       = 1,
        max_value       = 100
    ) 


    def __init__(self, participants, components, *args, **kwargs):

        super(ComponentSearchForm, self).__init__(participants, *args, **kwargs)

        self.fields["participants_field"].required  = False
        self.fields["participants_field"].widget    = forms.MultipleHiddenInput()

        if not components is None:
            self.components                         = components
            self.fields["components_field"].choices = EXTRA_CHOICES
            self.fields["components_field"].choices.extend(\
                [(comp.identifier, "Session %s - Component %s" % (comp.sessionId, comp)) for comp in components])


    def get_speaker_no(self):
        if self.is_valid():
            return self.cleaned_data["speaker_no_field"]
        else:
            return self.DEFAULT_SPEAKER_QUANTITY


    def return_selected_components(self):

        results = []

        if u'all' in self.cleaned_data["components_field"]:
            results = self.components
        else:
            for component in self.components:
                if component.identifier in self.cleaned_data["components_field"]:
                    results.append(component)

            
        return results