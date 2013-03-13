from django import forms

from search.forms.participant_search    import ParticipantSearchForm
from search.forms.choice_options        import *


class ParticipantComponentSearchForm(ParticipantSearchForm):

    components_field = forms.MultipleChoiceField (
        widget          = forms.CheckboxSelectMultiple,
        error_messages  = { 'required': 'Please select from the following list of components'},
        label           = "Components")


    def __init__(self, participants, components, *args, **kwargs):
        super(ParticipantComponentSearchForm, self).__init__(*args, **kwargs)

        self.participants   = participants
        self.components     = components

        if not components is None:
            self.fields["components_field"].choices = \
                [(comp.identifier, "Session %s - Component %s" % (comp.sessionId, comp)) for comp in components]
