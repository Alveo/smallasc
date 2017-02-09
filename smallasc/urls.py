from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

#URL Imports
import baseapp.views.dashboard
import baseapp.views.security
import baseapp.views.sparql
import django.contrib.auth.views


#from registration.backends.default.views import RegistrationView

#from registration.backends.default.views import RegistrationView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = [

	# The following urls are not handled as actual applications
	# Instead each url maps to a function which handles the request
	url (r'^$', baseapp.views.dashboard.index, name="baseapp.views.dashboard.index"),
    url (r'^login/$', django.contrib.auth.views.login, name="django.contrib.auth.views.login"),
    url (r'^logout/$', baseapp.views.security.logout_page, name="baseapp.views.security.logout_page"),
    #url (r'^register/$', 'baseapp.views.registration.register_page'),

    url (r'^browse/', include ('browse.urls')),
	url (r'^search/', include('search.urls')), 

    # pseudo SSO authentication module
	url (r'^sso/', include('sso.urls')), 

	url(r'^stats/', include('stats.urls')),
	url(r'^pages/', include('django.contrib.flatpages.urls')),


	#OAuth 2.0
	url(r'^oauth/callback', baseapp.views.security.oauth_callback, name="baseapp.views.security.oauth_callback"),
	#url(r'^oauth/validate', 'baseapp.views.security.oauth_validate'),

	# django-registration
 
	url(r'^registration/', include('registration.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url (r'^admin/', include(admin.site.urls)),

    # Url routing for the Participant Portal
    url (r'^participantportal/', include('participantportal.urls')),
    
    # SPARQL endpoint
    url(r'^sparql/', baseapp.views.sparql.sparql_endpoint, name="baseapp.views.sparql.sparql_endpoin"),

    # on-site editing of flat pages
    url(r'^tinymce/', include('tinymce.urls')),
    
    url(r'^accounts/', include('allauth.urls'))
]
