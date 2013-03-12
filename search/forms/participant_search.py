from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from browse.modelspackage.participants import Participant

EDUCATION_LEVELS = (('any', 'Any'),
              ('primary to junior high', 'Primary School to Junior High School'),
              ('school certificate', 'Junior Secondary (up to School Certificate level)'),
              ('higher school certificate', 'Senior Secondary (Higher School Certificate)'),
              ('TAFE Certificate', 'TAFE Certificate'),
              ('Diploma', 'Diploma'),
              ('Advanced Diploma', 'Advanced Diploma'),
              ('Associate Degree', 'Associate Degree'),
              ('Bachelor Degree', 'Bachelor Degree'),
              ('Vocational Graduate Certificate', 'Vocational Graduate Certificate'),
              ('Vocational Graduate Diploma', 'Vocational Graduate Diploma'),
              ('Graduate Certificate', 'Graduate Certificate'),
              ('Graduate Diploma', 'Graduate Diploma'),
              ('Masters Degree', 'Masters Degree'),
              ('Doctoral Degree', 'Doctoral Degree'),
            )

ENROLLMENT_TYPES = (('any', 'Any'),
              ('fulltime', 'Full Time'),
              ('parttime', 'Part Time'),
            )

PROFESSIONAL_CATEGORIES = (('any', 'Any'),
              ("manager and admin", "Managers and Administrators (e.g. school principal, judge, farm manager)"),
              ("professional", "Professionals (e.g. doctors, engineer, architect, scientist, teacher)"),
              ("assoc professional", "Associate professionals (e.g. police officer, nurse, ambulance driver)"),
              ("tradesperson", "Tradespersons and related workers (e.g. mechanic, plumber, baker)"),
              ("clerical and service", "Advanced clerical and service workers (e.g. secretary, insurance agent)"),
              ("intermediate clerical and service", "Intermediate clerical, sales and service workers (e.g. receptionist, teacher's aide)"),
              ("intermediate production", "Intermediate production and transport workers (e.g. miner, truck driver)"),
              ("elementary clerical", "Elementary clerical, sales and service workers (e.g. filing clerk, sales assistant)"),
              ("labourer", "Labourers and related workers (e.g. farm hand, fast food cook, handyperson)"),
              ("home duties", "Home duties"),
              ("unemployed", "Unemployed"),
            )

CULTURAL_HERITAGES = (('any', 'Any'),
              ("Australian", "Australian"),
              ("Aboriginal Australian", "Aboriginal Australian"),
              ("Other", "Other"),
            )

GENDER_CHOICES = (('any', 'Any'), ('male', 'Male'), ('female', 'Female'))
SES_CHOICES = (('any', 'Any'), ('Professional', 'Professional'), ('Non-Professional', 'Non-Professional'))
EXTRA_CHOICES = [('all', 'All')]

class ParticipantSearchForm(forms.Form):

    gender = forms.ChoiceField (label = "Gender", choices = GENDER_CHOICES)
    ses = forms.ChoiceField (label = 'Socio Economic Status', choices = SES_CHOICES)
    highest_qual = forms.ChoiceField (label = 'Highest Qualification', choices = EDUCATION_LEVELS)
    prof_cat = forms.ChoiceField (label = 'Professional Category', choices = PROFESSIONAL_CATEGORIES)

    def generate_predicates(self):
        predicates = {}
        if self.is_valid():
            if not self.cleaned_data['gender'] == 'any': predicates["foaf:gender"] = self.cleaned_data['gender'] 
            if not self.cleaned_data['ses'] == 'any': predicates["austalk:ses"] = self.cleaned_data['ses']
            if not self.cleaned_data['highest_qual'] == 'any': predicates["austalk:education_level"] = self.cleaned_data['highest_qual']
            if not self.cleaned_data['prof_cat'] == 'any': predicates["austalk:professional_category"] = self.cleaned_data['prof_cat']

        return predicates

    def url (self):
        return "/search/results/participants"


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


    def url (self):
        return "/search/results/participants/components"


class ParticipantComponentSearchForm(ParticipantSearchFilterForm):

    components_field = forms.MultipleChoiceField (
        widget = forms.CheckboxSelectMultiple,
        error_messages = { 'required': 'Please select from the following list of components'},
        label = "Components")


    def __init__(self, participants, components, *args, **kwargs):
        super(ParticipantComponentSearchForm, self).__init__(participants, *args, **kwargs)
        if not components is None:
            self.fields["components_field"].choices = [(comp.identifier, "Session %s - Component %s" % (comp.sessionId, comp)) for comp in components]