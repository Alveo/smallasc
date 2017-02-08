from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

import browse.views.sites
import browse.views.agreements
import browse.views.participants
import browse.views.components
import browse.views.items

urlpatterns = [
    url (r'^$', browse.views.sites.index),
    url (r'^agreements/$', browse.views.agreements.index),
    url (r'^participant/(\w+)/$', browse.views.participants.show_by_id),
    url (r'^(\w+)/$', browse.views.participants.index),
    url (r'^(\w+)/(\w+)/$', browse.views.participants.show),
    url (r'^(\w+)/(\w+)/(\w+)/$', browse.views.components.index),
    url (r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/$', browse.views.items.index),
    url (r'^(\w+)/(\w+)/(\w+)/(.+)/([0-9_]+)$', browse.views.items.show)
]
