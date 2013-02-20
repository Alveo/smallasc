from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

# Generic patterns for search
urlpatterns = patterns('search.views',
    url (r'^$', 'index'),
    url (r'^results/$', 'prompt.search'),
    url (r'^results/participants/$', 'participants.search'),
    url (r'^results/participants/components/$', 'components.search'),
)
