from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth import authenticate
import pyalveo

def logout_page (request, redirect_url = '/'):
	logout (request)
	return HttpResponseRedirect(redirect_url)


def oauth_callback(request, redirect_url= '/'):
	client = request.session.get('client',None)
	
	if client==None:
		return HttpResponseRedirect(redirect_url)
	
	client.oauth.on_callback(request.build_absolute_uri())
	
	
	return HttpResponseRedirect(redirect_url)
	
	
def oauth_login(request, redirect_url= '/'):
	
	client = request.session.get('client',None)
	
	if client != None:
		if client.oauth.validate():
			return HttpResponseRedirect(redirect_url)
	
	client = pyalveo.Client(api_url=settings.API_URL,client_id=settings.OAUTH_CLIENT_ID,
						client_secret=settings.OAUTH_CLIENT_SECRET,redirect_url=settings.OAUTH_REDIRECT_URL,verifySSL=False)
	url = client.oauth.get_authorisation_url()
	request.session['client'] = client
	redirect_url = url
	return HttpResponseRedirect(redirect_url)