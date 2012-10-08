from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

# Generic patterns for search
urlpatterns = patterns('search.views',
    url (r'^$', 'composite.index'),
    url (r'^sites/$', 'sites.index'),
    url (r'^sites/(\w+)/participants/$', 'participants.index'),
    url (r'^sites/(\w+)/participants/(\w+)/$', 'participants.show'),
    url (r'^sites/(\w+)/participants/(\w+)/sessions/(\w+)/components', 'components.index'),
    url (r'^results/$', 'composite.search')
)
