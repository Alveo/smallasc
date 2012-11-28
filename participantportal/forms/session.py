from datetime import date
from django import forms
from django.forms.widgets import Select, RadioSelect

from baseapp.modelspackage.animals import Animal
from baseapp.modelspackage.colours import Colour

# This tuple is defined elsewhere but I am not comfortable
# using that tuple unless they are all unified in one place
# otherwise we have too strong a coupling between the applications
GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

def get_years():
  current_year = date.today().year
  return ((i, i) for i in range(current_year - 100, current_year - 18))

class LoginForm(forms.Form):

  animal      = forms.ModelChoiceField(queryset = Animal.objects.order_by('name'), initial = 1)
  colour      = forms.ModelChoiceField(queryset = Colour.objects.all(), initial = 1, 
    widget = Select(attrs={'class':'input-medium'}))
  birth_year  = forms.ChoiceField(choices = get_years(), widget = Select(attrs={'class':'input-medium'}))
  gender = forms.ChoiceField(choices = GENDER_CHOICES, widget = RadioSelect, initial = 'M')