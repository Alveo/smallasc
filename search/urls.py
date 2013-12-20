from django.conf.urls 		import patterns, include, url


urlpatterns = patterns('search.views',
    url (r'^$', 'participants.search'),
    url (r'^prompt/', 'prompt.search'),
    url (r'^participants/$', 'participants.filter'),
    url (r'^participants/components/$', 'components.search'),
)
