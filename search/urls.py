from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView


urlpatterns = patterns('search.views',
    url (r'^$', 'composite.index'),
)
