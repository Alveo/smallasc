from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

# Generic patterns for search
urlpatterns = patterns('search.views',
    url (r'^$', 'index'),
    url (r'^results/$', 'prompt.prompt_search'),
    url (r'^results/participants/$', 'prompt.participant_search'),
    url (r'^results/items/$', 'item_search'),
)
