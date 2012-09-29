import re
from django import forms
from django.forms.widgets import RadioSelect
from django.contrib.auth.models import User

# Definition for new user registration form
class RegistrationForm(forms.Form):
	# Registration form field definitions
	user_name = forms.CharField (widget = forms.TextInput (attrs = {'size': '30', 'maxlength':'30'}))
	first_name = forms.CharField (widget = forms.TextInput (attrs = {'size':'30','maxlength':'30'}))
	last_name = forms.CharField (widget = forms.TextInput (attrs = {'size':'30','maxlength':'30'}))
	email = forms.EmailField (widget = forms.TextInput (attrs = {'size':'30','maxlength':'75'}))
	password_original = forms.CharField (widget = forms.PasswordInput())
	password_confirm = forms.CharField (widget = forms.PasswordInput())

	# Check to make sure that username follows certain rules and it not in use
	def clean_user_name(self):
		user_name = self.cleaned_data['user_name']
		if not re.search (r'^\w+$', user_name):
			raise forms.ValidationError ('Username can only contain alphanumeric characters and the underscore.')
		try:
			User.objects.get (username = user_name)
		except User.DoesNotExist:
			return user_name
			
		raise forms.ValidationError ('A user has already registered with that username.')
	
	def clean_email(self):
		email = self.cleaned_data['email']
		
		try:
			User.objects.get (email = email)
		except User.DoesNotExist:
			return email
			
		raise forms.ValidationError ('A user has already registered with that email address.')
	
	def clean_password_confirm(self):
		""" Check to make sure that the two passwords match """
		if 'password_original' in self.cleaned_data:
			password1 = self.cleaned_data['password_original']
			password2 = self.cleaned_data['password_confirm']
			if password1 == password2:
				return password2
		
		raise forms.ValidationError ('Passwords do not match.')