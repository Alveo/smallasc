from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.conf import settings

def logout_page (request, redirect_url = '/'):
	logout (request)
	return HttpResponseRedirect(redirect_url)


def oauth_callback(request, redirect_url= '/'):
	settings.PYALVEO_CLIENT.oauth.on_callback(request.build_absolute_uri())
	
