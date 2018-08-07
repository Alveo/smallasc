from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, Group,Permission,ContentType
import pyalveo
import urlparse
from datetime import datetime

def logout_page (request, redirect_url = '/'):
	logout (request)
	return HttpResponseRedirect(redirect_url)



def create_group_with_perms():
	
	g = Group.objects.create(name='research')
	ct = ContentType.objects.get(app_label='auth', model='user')
	
	permissions = ['can_view_dashboard','can_view_agreements','can_view_components',
					'can_view_items','can_view_item','can_view_participants',
					'can_view_participant','can_view_sites','can_view_item_search',
					'can_view_participant_search','can_view_prompt_search']
	
	for i in permissions:
		p,created = Permission.objects.get_or_create(codename=i,name=i.replace('_',' '),content_type=ct)
		g.permissions.add(p)
	g.save()
	return g

def apikey_login(request, redirect_url= '/'):
	
	request.session.flush()
	client = request.session.get('client',None)
	
	#If there a client exists and is valid, don't bother doing anything, redirect home.
	if client != None:
		if client.oauth.validate():
			return HttpResponseRedirect(redirect_url)
	
	OAUTH = {
         'client_id':settings.OAUTH_CLIENT_ID,
         'client_secret':settings.OAUTH_CLIENT_SECRET,
         'redirect_url':settings.OAUTH_REDIRECT_URL
         }
	
	apiKey = request.GET.get("apikey",None)
	
	client = pyalveo.Client(api_url=settings.API_URL,api_key=apiKey,oauth=OAUTH,verifySSL=False)
	
	#Get user details
	res = client.oauth.get_user_data()
	
	if not res:
		HttpResponseRedirect(redirect_url)
	
	
	request.session['client'] = client.to_json()
	
	#sign in member if exists, else create
	#Later should check that their status is 'A' or whichever codes are valid.
	
	password = "%s123"%res['last_name']
	username = "%s%s" % (res['first_name'],res['last_name'])
	admin = res.get('role','')=="admin"
	
	try:
		user = User.objects.get(username=username)
	except:
		user = None
	
	#The user logged in at Alveo so they must exist here.
	if user is not None:
		#Already exist so just login
		login(request,user,backend="django.contrib.auth.backends.ModelBackend")
	else:
		#Doesn't exist, so create a new account and login.
		now = datetime.now()
		user = User.objects.create(username=username,
										email=res['email'],
										first_name=res['first_name'],
										last_name=res['last_name'],
										password=password,
										last_login=now,
										date_joined=now,
										is_staff = admin, 
										is_active = True, 
										is_superuser = admin)
		
		try:
			g = Group.objects.get(name='research')
		except:
			g = create_group_with_perms()
			
  		g.user_set.add(user)
  		user.save()
		if user is not None:
			login(request,user,backend="django.contrib.auth.backends.ModelBackend")
	
	return HttpResponseRedirect(redirect_url)


def oauth_callback(request, redirect_url= '/'):
	client = pyalveo.Client.from_json(request.session.get('client',None))
	
	if client==None:
		return HttpResponseRedirect(redirect_url)
	
	client.oauth.on_callback(request.build_absolute_uri())
	
	#Get user details
	res = client.oauth.get_user_data()
	
	request.session['client'] = client.to_json()
	
	#sign in member if exists, else create
	#Later should check that their status is 'A' or whichever codes are valid.
	
	password = "%s123"%res['last_name']
	username = "%s%s" % (res['first_name'],res['last_name'])
	admin = res.get('role','')=="admin"
	
	try:
		user = User.objects.get(username=username)
	except:
		user = None
	
	#The user logged in at Alveo so they must exist here.
	if user is not None:
		#Already exist so just login
		login(request,user,backend="django.contrib.auth.backends.ModelBackend")
	else:
		#Doesn't exist, so create a new account and login.
		now = datetime.now()
		user = User.objects.create(username=username,
										email=res['email'],
										first_name=res['first_name'],
										last_name=res['last_name'],
										password=password,
										last_login=now,
										date_joined=now,
										is_staff = admin, 
										is_active = True, 
										is_superuser = admin)
		
		try:
			g = Group.objects.get(name='research')
		except:
			g = create_group_with_perms()
			
  		g.user_set.add(user)
  		user.save()
		if user is not None:
			login(request,user,backend="django.contrib.auth.backends.ModelBackend")
	
	redirect_url = request.session.get('next', redirect_url)
	
	return HttpResponseRedirect(redirect_url)
	
	
def oauth_logout(request, redirect_url= '/'):
	request.session.flush()	
	return HttpResponseRedirect(redirect_url)
	
def oauth_login(request, redirect_url= '/'):
	
	request.session.flush()
	client = request.session.get('client',None)
	
	#If there a client exists and is valid, don't bother doing anything, redirect home.
	if client != None:
		if client.oauth.validate():
			return HttpResponseRedirect(redirect_url)
	
	redirect_url = '%s/oauth/callback' % request.get_host()
	
	OAUTH = {
         'client_id':settings.OAUTH_CLIENT_ID,
         'client_secret':settings.OAUTH_CLIENT_SECRET,
         'redirect_url':redirect_url,
         }
	
	client = pyalveo.Client(api_url=settings.API_URL,oauth=OAUTH,verifySSL=False)
	url = client.oauth.get_authorisation_url()
	request.session['client'] = client.to_json()
	
	request.session['next'] = request.GET.get('next', redirect_url)
	
	redirect_url = url
	return HttpResponseRedirect(redirect_url)


