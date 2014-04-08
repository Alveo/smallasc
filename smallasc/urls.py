from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView


#from registration.backends.default.views import RegistrationView

#from registration.backends.default.views import RegistrationView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# The following urls are not handled as actual applications
	# Instead each url maps to a function which handles the request
	url (r'^$', 'baseapp.views.dashboard.index'),
    url (r'^login/$', 'django.contrib.auth.views.login'),
    url (r'^logout/$', 'baseapp.views.security.logout_page'),
    #url (r'^register/$', 'baseapp.views.registration.register_page'),

    # The search module at present handles both browse and
    # search, perhaps the module should be renamed?
    url (r'^browse/', include ('browse.urls')),
	url (r'^search/', include('search.urls')), 

    # pseudo SSO authentication module
	url (r'^sso/', include('sso.urls')), 

	url(r'^stats/', include('stats.urls')),
	url(r'^pages/', include('django.contrib.flatpages.urls')),

	# django-registration

    
 
	url(r'^registration/', include('registration.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url (r'^admin/', include(admin.site.urls)),

    # Url routing for the Participant Portal
    url (r'^participantportal/', include('participantportal.urls')),
    
    # SPARQL endpoint
    url(r'^sparql/', 'baseapp.views.sparql.sparql_endpoint'),
)
