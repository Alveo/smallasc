from django.conf.urls import include, url
from django.views.generic import DetailView, ListView

import browse.views.sites
import browse.views.agreements
import browse.views.participants
import browse.views.components
import browse.views.items

urlpatterns = [
    url (r'^$', browse.views.sites.index, name="browse.views.sites.index"),
    url (r'^agreements/$', browse.views.agreements.index, name="browse.views.agreements.index"),
    url (r'^participant/(\w+)/$', browse.views.participants.show_by_id, name="browse.views.participants.show_by_id"),
    url (r'^(\w+)/$', browse.views.participants.index, name="browse.views.participants.index"),
    url (r'^(\w+)/(\w+)/$', browse.views.participants.show, name="browse.views.participants.show"),
    url (r'^(\w+)/(\w+)/(\w+)/$', browse.views.components.index, name="browse.views.components.index"),
    url (r'^(\w+)/(\w+)/(\w+)/([a-z0-9-]+)/$', browse.views.items.index, name="browse.views.items.index"),
    url (r'^(\w+)/(\w+)/(\w+)/(.+)/([0-9_]+)$', browse.views.items.show, name="browse.views.items.show")
]
