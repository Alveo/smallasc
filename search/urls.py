from django.conf.urls import include, url

from django.views.generic import TemplateView

import search.views.prompt
import search.views.participants
import search.views.components

urlpatterns = [
    url (r'^$', TemplateView.as_view(template_name='search/index.html')),
    url (r'^prompt/', 
         search.views.prompt.search, 
         name="search.views.prompt.search"),
    url (r'^participants/$', 
         search.views.participants.search, 
         name="search.views.participants.search"),
    url (r'^participants/filter/$', 
         search.views.participants.filter, 
         name="search.views.participants.filter"),
    url (r'^participants/components/$', 
         search.views.components.search, 
         name="search.views.components.search")
]
