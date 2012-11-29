from django.conf.urls import patterns, include, url
from baseapp.views.security import logout_page

urlpatterns = patterns('participantportal.views',
  url(r'^$', 'home.index'),
  url(r'^login/$', 'session.login_page'),
  url(r'^logout/$', 'session.logout_page')
)
