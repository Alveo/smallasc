from django import forms
from django.forms.widgets import CheckboxSelectMultiple

# Models in use
from search.models.sites import Sites

class CompositeSearchForm (forms.Form):
	""" Form used to represent the composite search fields """
	sites = Sites.objects.all ()
	sites_field = forms.ModelMultipleChoiceField(widget=CheckboxSelectMultiple(),
												label = 'Recording Locations',
												required = True, 
												queryset = sites)