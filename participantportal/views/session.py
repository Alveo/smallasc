from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext

# Import forms
from participantportal.forms.session import LoginForm

def login_page(request):
  if request.method == 'POST':
    # When we receive the details we use our custom authenticator located in
    # the package participantportal.modelspackage.auth
    form = LoginForm(request.POST)
    if form.is_valid():
      # Our request should be routed to our custom authenticator
      # as configured in our AUTHENTICATION_BACKENDS field of settings.py
      user = authenticate(
        colour      = form.data['colour'], 
        animal      = form.data['animal'],
        birth_year  = form.cleaned_data['birth_year'],
        gender      = form.data['gender'])

      if user is not None:
        # The authenticator requires that a password is set, but the actual
        # password is not all that important
        login(request, user)
        return HttpResponseRedirect ('/participantportal/')
      else:
        form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
  else:
    form = LoginForm()

  variables = RequestContext(request, {'form': form})
  return render_to_response('login.html', variables)


def logout_page(request):
  logout (request)
  return HttpResponseRedirect ('/participantportal/login')