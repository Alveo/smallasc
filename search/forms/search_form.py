from django                         import forms
from search.forms.choice_options    import *


class SearchForm(forms.Form):

    speakerid       = forms.CharField(required = False, label = 'Speaker ID (eg. 1_123)')
    gender          = forms.ChoiceField(required = False, label = "Gender", choices = GENDER_CHOICES)
    agegroup        = forms.ChoiceField(required = False, label = 'Age', choices = AGEGROUP_CHOICES)
    recording_site  = forms.ChoiceField(required = False, label = 'Recording Site', choices = RECORDING_SITES)


    def generate_predicates(self):
        
        predicates = {}
        
        if self.is_valid():
            if not self.cleaned_data['gender'] == 'any': 
                predicates["foaf:gender"] = self.cleaned_data['gender'] 

            if not self.cleaned_data['agegroup'] == 'any': 
                predicates["austalk:ageGroup"] = self.cleaned_data['agegroup']

            if not self.cleaned_data['recording_site'] == 'any': 
                predicates["austalk:recording_site"] = self.cleaned_data['recording_site']

            if self.cleaned_data.has_key('speakerid') and self.cleaned_data['speakerid'] != '':
                predicates["austalk:id"] = self.cleaned_data['speakerid']

        return predicates


