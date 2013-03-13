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

