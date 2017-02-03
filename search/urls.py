from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

import search.views.prompt.search
import search.views.participants.search
import search.views.participants.filter
import search.views.components.search

urlpatterns = [
    url (r'^$', TemplateView.as_view(template_name='search/index.html')),
    url (r'^prompt/', search.views.prompt.search),
    url (r'^participants/$', search.views.participants.search),
    url (r'^participants/filter/$', search.views.participants.filter),
    url (r'^participants/components/$', search.views.components.search)
]
