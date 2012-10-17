from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

# Generic patterns for search
urlpatterns = patterns('browse.views',
    
    url (r'^$', 'sites.index'),
    url (r'^(\w+)/$', 'participants.index'),
    url (r'^(\w+)/(\w+)/$', 'participants.show'),
    url (r'^(\w+)/(\w+)/(\w+)/$', 'components.index'),
    url (r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/$', 'items.index'),
    url (r'^(\w+)/(\w+)/(\w+)/(.+)/([0-9_]+)$', 'items.show'),
    
    
    url (r'^results/$', 'composite.search')
)
