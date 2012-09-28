from django.conf.urls import patterns, include, url
from django.contrib import admin

from baseapp.views.dashboard import index

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	# Wire up each of the web applications
	url (r'^$', index),
	url (r'^search/', include ('search.urls')),
    url (r'^login/$', 'django.contrib.auth.views.login'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url (r'^admin/', include(admin.site.urls)),
)
