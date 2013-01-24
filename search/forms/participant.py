from django import forms
from django.forms.widgets import CheckboxSelectMultiple

# Models in use
from browse.modelspackage import Site
from browse.modelspackage import Protocol

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

PROFESSIONAL_CATEGORIES = (
                           ('any', 'Any'),
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


class ParticipantSearchForm (forms.Form):
    """ Form to find participants via demographic data"""

    gender = forms.ChoiceField(label="Gender", 
                               choices=GENDER_CHOICES
                               )
    ses = forms.ChoiceField(label='Socio Economic Status', 
                            choices = SES_CHOICES)
    
    highest_qual = forms.ChoiceField(label='Highest Qualification',
                                     choices=EDUCATION_LEVELS)
    
    prof_cat = forms.ChoiceField(label='Professional Category',
                                 choices=PROFESSIONAL_CATEGORIES)
    
    #first_language = forms.CharField(label='First Language')
    
    