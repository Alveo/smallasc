from django import forms

from search.forms.choice_options        import *
from search.forms.participant_search    import ParticipantSearchForm


class ParticipantSearchFilterForm(ParticipantSearchForm):
    
    participants_field = forms.MultipleChoiceField (
        widget          = forms.CheckboxSelectMultiple,
        error_messages  = { 'required': 'Please select from the following list of participants'},
        label           = "Participants")


    def __init__(self, participants, *args, **kwargs):
        super(ParticipantSearchFilterForm, self).__init__(*args, **kwargs)

        self.participants = participants

        if not participants is None:
            self.fields["participants_field"].choices = EXTRA_CHOICES
            self.fields["participants_field"].choices.extend([(part.friendly_id (), part) for part in participants])


    def return_selected_participants(self):

        results = []

        if u'all' in self.cleaned_data["participants_field"]:

            results = self.participants
        
        else:

            for participant in self.participants:
                if participant.friendly_id() in self.cleaned_data["participants_field"]:
                    results.append(participant)

        
        return results