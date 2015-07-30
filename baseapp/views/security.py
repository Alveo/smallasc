from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def logout_page (request, redirect_url = '/'):
	logout (request)
	return HttpResponseRedirect(redirect_url)


