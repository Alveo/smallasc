from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
import pyalveo

def logout_page (request, redirect_url = '/'):
	logout (request)
	return HttpResponseRedirect(redirect_url)


def oauth_callback(request, redirect_url= '/'):
	client = request.session.get('client',None)
	
	if client==None:
		return HttpResponseRedirect(redirect_url)
	
	client.oauth.on_callback(request.build_absolute_uri())
	
	request.session['client'] = client
	
	#Get user details
	res = client.oauth.get_user_data()
	
	#sign in member if exists, else create
	#Later should check that their status is 'A' or whichever codes are valid.
	
	password = "%s.123"%res['last_name']
	username = "%s %s" % (res['first_name'],res['last_name'])
	
	user = authenticate(username=username,password=password)
	
	#The user logged in at Alveo so they must exist here.
	if user is not None:
		#Already exist so just login
		login(request,user)
	else:
		#Doesn't exist, so create a new account and login.
		user = User.objects.create(username=username,
										email=res['email'],
										password=password)
		if user is not None:
			login(request,user)
	
	return HttpResponseRedirect(redirect_url)
	
	
def oauth_login(request, redirect_url= '/'):
	
	client = request.session.get('client',None)
	
	#If there a client exists and is valid, don't bother doing anything, redirect home.
	if client != None:
		if client.oauth.validate():
			return HttpResponseRedirect(redirect_url)
	
	client = pyalveo.Client(api_url=settings.API_URL,client_id=settings.OAUTH_CLIENT_ID,
						client_secret=settings.OAUTH_CLIENT_SECRET,redirect_url=settings.OAUTH_REDIRECT_URL,verifySSL=False)
	url = client.oauth.get_authorisation_url()
	request.session['client'] = client
	redirect_url = url
	return HttpResponseRedirect(redirect_url)