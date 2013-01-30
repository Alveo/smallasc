from django.conf.urls import patterns, include, url
from baseapp.views.security import logout_page

urlpatterns = patterns('participantportal.views',
  url(regex = r'^$', view = 'data.index', name = 'home', kwargs = { 'template': 'home.html' }, ),
  url(r'^data/$', 'data.index'),
  url(r'^termsandconditions/$', 'termsandconditions.index'),
  url (r'^(\w+)/(\w+)/(\w+)/$', 'components.index'),
  url (r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/$', 'items.index'),
  url (r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/([0-9_]+)/$', 'items.show'),
  url(r'^login/$', 'session.login_page'),
  url(regex = r'^logout/$', view = 'logout_page', name = 'session', kwargs = { 'redirect_url' : '/participantportal/login'}, )
)
