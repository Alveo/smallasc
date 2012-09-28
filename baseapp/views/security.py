from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def logout_page (request):
	""" This function ends a users login session and re-directs the user back render_to_response
	to the login page. """
	logout (request)
	return HttpResponseRedirect ('/login')


