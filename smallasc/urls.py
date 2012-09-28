from django.conf.urls import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# Wire up each of the web applications
	url (r'^$', 'baseapp.views.dashboard.index'),
    url (r'^login/$', 'django.contrib.auth.views.login'),
    url (r'^logout/$', 'baseapp.views.security.logout_page'),

    # Routing handled by available apps
	url (r'^search/', include ('search.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url (r'^admin/', include(admin.site.urls)),
)
