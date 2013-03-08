from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# The following urls are not handled as actual applications
	# Instead each url maps to a function which handles the request
	url (r'^$', 'baseapp.views.dashboard.index'),
    url (r'^login/$', 'django.contrib.auth.views.login'),
    url (r'^logout/$', 'baseapp.views.security.logout_page'),
    url (r'^register/$', 'baseapp.views.registration.register_page'),

    # The search module at present handles both browse and
    # search, perhaps the module should be renamed?
    url (r'^browse/', include ('browse.urls')),
	url (r'^search/', include('search.urls')), 

    # pseudo SSO authentication module
	url (r'^sso/', include('sso.urls')), 

    # sample stats pages
	url(r'^stats/query/$', TemplateView.as_view(template_name='sgvizler.html')),
	url(r'^stats/$', TemplateView.as_view(template_name='p_report.html')),

	url(r'^pages/', include('django.contrib.flatpages.urls')),


    # Uncomment the next line to enable the admin:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url (r'^admin/', include(admin.site.urls)),

    # Url routing for the Participant Portal
    url (r'^participantportal/', include('participantportal.urls')),
)
