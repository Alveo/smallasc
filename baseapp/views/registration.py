from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User

# Import forms
from baseapp.forms.registration import RegistrationForm

def register_page (request):
	""" This view is for registering a new user """	
	if request.method == 'POST':

		form = RegistrationForm (request.POST)
		if form.is_valid():
		
			user = User.objects.create_user (
				username = form.cleaned_data['user_name'],
				password = form.cleaned_data['password_original'],
				email = form.cleaned_data['email']
				)
						
			return render (request, "registration/register_success.html")
	else:

		form = RegistrationForm ()

	variables = RequestContext (request, {'form': form})
	return render_to_response ('registration/register.html', variables)