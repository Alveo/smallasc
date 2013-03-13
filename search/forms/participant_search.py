from django import forms
from search.forms.choice_options import *


class ParticipantSearchForm(forms.Form):

    gender          = forms.ChoiceField (label = "Gender", choices = GENDER_CHOICES)
    ses             = forms.ChoiceField (label = 'Socio Economic Status', choices = SES_CHOICES)
    highest_qual    = forms.ChoiceField (label = 'Highest Qualification', choices = EDUCATION_LEVELS)
    prof_cat        = forms.ChoiceField (label = 'Professional Category', choices = PROFESSIONAL_CATEGORIES)


    def generate_predicates(self):
        
        predicates = {}
        
        if self.is_valid():
            if not self.cleaned_data['gender'] == 'any': 
                predicates["foaf:gender"] = self.cleaned_data['gender'] 

            if not self.cleaned_data['ses'] == 'any': 
                predicates["austalk:ses"] = self.cleaned_data['ses']

            if not self.cleaned_data['highest_qual'] == 'any': 
                predicates["austalk:education_level"] = self.cleaned_data['highest_qual']

            if not self.cleaned_data['prof_cat'] == 'any': 
                predicates["austalk:professional_category"] = self.cleaned_data['prof_cat']

        return predicates


class ParticipantSearchFilterForm(ParticipantSearchForm):
    
    participants_field = forms.MultipleChoiceField (
        widget = forms.CheckboxSelectMultiple,
        error_messages = { 'required': 'Please select from the following list of participants'},
        label = "Participants")


    def __init__(self, participants, *args, **kwargs):
        super(ParticipantSearchFilterForm, self).__init__(*args, **kwargs)

        self.participants = participants

        if not participants is None:
            self.fields["participants_field"].choices = EXTRA_CHOICES
            self.fields["participants_field"].choices.extend([(part.friendly_id (), part) for part in participants])


    def return_selected_participants(self):

        if u'all' in self.cleaned_data["participants_field"]:
            return [part.friendly_id() for part in self.participants]
        else:
            return self.cleaned_data["participants_field"]
