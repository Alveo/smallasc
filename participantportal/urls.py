from django.conf.urls import patterns, include, url
from baseapp.views.security import logout_page

urlpatterns = patterns('participantportal.views',
  url(r'^$', 'home.index'),
  url (r'^(\w+)/(\w+)/(\w+)/$', 'components.index'),
  url (r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/$', 'items.index'),
  url (r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/([0-9_]+)/$', 'items.show'),
  url(r'^login/$', 'session.login_page'),
  url(r'^logout/$', 'session.logout_page')
)
