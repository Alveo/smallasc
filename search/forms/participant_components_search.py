from django import forms

from search.forms.participant_search    import ParticipantSearchForm
from search.forms.choice_options        import *


class ParticipantComponentSearchForm(ParticipantSearchForm):

    participants_field  = forms.MultipleChoiceField(
        widget          = forms.CheckboxSelectMultiple)

    components_field    = forms.MultipleChoiceField (
        widget          = forms.CheckboxSelectMultiple,
        error_messages  = { 'required': 'Please select from the following list of components'},
        label           = "Components")


    def __init__(self, participants, components, *args, **kwargs):
        super(ParticipantComponentSearchForm, self).__init__(*args, **kwargs)

        if not participants is None:         
            self.participants                         = participants
            self.fields["participants_field"].choices = [(part.friendly_id (), part) for part in participants]


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