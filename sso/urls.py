from django.conf.urls import patterns, include, url

# Generic patterns for search
urlpatterns = patterns('sso.views',
    url (r'^sessions/$', 'is_valid_session', name='sso:is_valid_session'),
    url (r'^tsessions/$', 'is_valid_tsession', name='sso:is_valid_tsession'),
    url (r'^login/$', 'login', name='sso:login'),

    url(r'^test/$', 'test_embedded'),   # DEBUG
)
