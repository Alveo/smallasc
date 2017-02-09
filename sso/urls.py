from django.conf.urls import include, url
from sso.views import is_valid_session,is_valid_tsession,login,test_embedded
# Generic patterns for search
urlpatterns = [
    url (r'^sessions/$', is_valid_session, name='sso_is_valid_session'),
    url (r'^tsessions/$', is_valid_tsession, name='sso_is_valid_tsession'),
    url (r'^login/$', login, name='sso_login'),

    url(r'^test/$', test_embedded, name='sso_test_embedded')   # DEBUG
]