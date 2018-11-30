from datetime import date
from django import forms
from django.forms.widgets import Select, RadioSelect
from django.conf import settings

from baseapp.modelspackage.animals import Animal
from baseapp.modelspackage.colours import Colour
from browse.modelspackage.sites import SiteManager, Site

from itertools import chain

# This tuple is defined elsewhere but I am not comfortable
# using that tuple unless they are all unified in one place
# otherwise we have too strong a coupling between the applications
GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))

EDUCATION_LEVEL_CHOICES = ((None, 'Unknown'),
							('primary to junior high', 'Primary to Junior High'),
							('school certificate', 'School Certificate'),
							('Bachelor Degree','Bachelor Degree' ),
							('higher school certificate', 'Higher School Certificate'),
							('Diploma', 'Diploma'),
							('Graduate Certificate', 'Graduate Certificate'),
							('Advanced Diploma', 'Advanced Diploma'),
							('Masters Degree', 'Masters Degree'),
							('Vocational Graduate Certificate','Vocational Graduate Certificate'),
							('Vocational Graduate Diploma', 'Vocational Graduate Diploma'),
							('Doctoral Degree', 'Doctoral Degree'),
							('Associate Degree', 'Associate Degree'),
							('TAFE Certificate', 'TAFE Certificate'),
							('Graduate Diploma', 'Graduate Diploma')
						)


def get_years():
  current_year = date.today().year
  return ((i, i) for i in range(current_year - 100, current_year - 18))

def get_sites():
	siteManager = SiteManager(client_json=settings.PPCLIENT)
	sites =  siteManager.all()
	choices = []
	for site in sites:
		choices.append((site.label,site.name))
	return choices

class LoginForm(forms.Form):

  animal      = forms.ModelChoiceField(queryset = Animal.objects.order_by('name'), initial = 1, widget = Select(attrs={'class':'form-control'}))
  colour      = forms.ModelChoiceField(queryset = Colour.objects.all(), initial = 1, widget = Select(attrs={'class':'form-control'}))
  birth_year  = forms.ChoiceField(choices = get_years(), widget = Select(attrs={'class':'form-control'}))
  gender = forms.ChoiceField(choices = GENDER_CHOICES, widget = RadioSelect, initial = 'male')


#class Password_Reset_Form(forms.Form):
class ColourAnimalHelperForm(forms.Form):
	pwd_site = forms.ChoiceField(choices = get_sites(), widget= Select(attrs={'class':'form-control'}))
	pwd_highest_qual = forms.ChoiceField(choices = sorted(EDUCATION_LEVEL_CHOICES), widget=Select(attrs={'class':'form-control'}), required=False)
	pwd_father_highest_qual = forms.ChoiceField(choices = sorted(EDUCATION_LEVEL_CHOICES), widget=Select(attrs={'class':'form-control'}), required=False)
	pwd_mother_highest_qual = forms.ChoiceField(choices = sorted(EDUCATION_LEVEL_CHOICES), widget=Select(attrs={'class':'form-control'}), required=False)
	