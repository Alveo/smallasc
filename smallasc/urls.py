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
    url (r'^browse/', include ('search.urls')),
	url (r'^search/', include ('search.urls')),

    # download/data app
    url (r'^data/', include ('data.urls', namespace="data", app_name="data")),


	url(r'^report/$', TemplateView.as_view(template_name='sgvizler.html')),
	url(r'^report/participants$', TemplateView.as_view(template_name='p_report.html')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url (r'^admin/', include(admin.site.urls)),
)
