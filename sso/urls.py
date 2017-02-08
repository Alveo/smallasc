from django.conf.urls import patterns, include, url
from sso.views import is_valid_session,is_valid_tsession,login,test_embedded
# Generic patterns for search
urlpatterns = [
    url (r'^sessions/$', is_valid_session, name='sso:is_valid_session'),
    url (r'^tsessions/$', is_valid_tsession, name='sso:is_valid_tsession'),
    url (r'^login/$', login, name='sso:login'),

    url(r'^test/$', test_embedded)   # DEBUG
]