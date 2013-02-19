from django.conf.urls import patterns, include, url
from browse.views import components

urlpatterns = patterns('',
  url(regex = r'^$', 
      view = 'participantportal.views.data.index', 
      name = 'home', 
      kwargs = { 'template': 'home.html' }, ),
  
  url(r'^data/$', 'participantportal.views.data.index'),
  
  url(r'^termsandconditions/$', 'participantportal.views.termsandconditions.index'),
  
  url(regex = r'^(\w+)/(\w+)/(\w+)/$', 
      view = 'browse.views.components.index', 
      name = 'components', 
      kwargs = { 'template': 'participantportal/components/index.html'}, ),

  url(regex = r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/$', 
      view = 'browse.views.items.index', 
      name = 'items list', 
      kwargs = { 'template': 'participantportal/items/index.html'}, ),

  url(regex = r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/([0-9_]+)/$', 
      view = 'browse.views.items.show',
      name = 'items show',
      kwargs = { 'template': 'participantportal/items/show.html'}, ),
  
  url(r'^login/$', 'participantportal.views.session.login_page'),
  
  url(regex = r'^logout/$', 
      view = 'baseapp.views.security.logout_page', 
      name = 'session', 
      kwargs = { 'redirect_url' : '/participantportal/login'}, )
)
