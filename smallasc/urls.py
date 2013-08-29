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
    #url (r'^register/$', 'baseapp.views.registration.register_page'),

    # The search module at present handles both browse and
    # search, perhaps the module should be renamed?
    url (r'^browse/', include ('browse.urls')),
	url (r'^search/', include('search.urls')), 

    # pseudo SSO authentication module
	url (r'^sso/', include('sso.urls')), 

    # sample stats pages
	url(r'^stats/query/$', TemplateView.as_view(template_name='statistics/sgvizler.html')),
	url(r'^stats/age.html$', TemplateView.as_view(template_name='statistics/age.htm')),
	url(r'^stats/birthplaces.html$', TemplateView.as_view(template_name='statistics/birthplaces.htm')),
	url(r'^stats/culture.html$', TemplateView.as_view(template_name='statistics/culture.htm')),
	url(r'^stats/gender.html$', TemplateView.as_view(template_name='statistics/gender.htm')),
	url(r'^stats/help.html$', TemplateView.as_view(template_name='statistics/help_page.htm')),
	url(r'^stats/language.html$', TemplateView.as_view(template_name='statistics/language.htm')),
	url(r'^stats/professional_category.html$', TemplateView.as_view(template_name='statistics/professional_category.htm')),
	url(r'^stats/query.html$', TemplateView.as_view(template_name='statistics/query.htm')),
	url(r'^stats/stats.html$', TemplateView.as_view(template_name='statistics/stats.htm')),
	url(r'^stats/$', TemplateView.as_view(template_name='statistics/p_report.html')),

	url(r'^pages/', include('django.contrib.flatpages.urls')),

	# django-registration
	#url(r'^accounts/', include('registration.backends.default.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url (r'^admin/', include(admin.site.urls)),

    # Url routing for the Participant Portal
    url (r'^participantportal/', include('participantportal.urls')),
)
