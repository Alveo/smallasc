from django.conf.urls import patterns, include, url


from django.views.generic import TemplateView


urlpatterns = patterns('search.views',
    url (r'^$', TemplateView.as_view(template_name='search/index.html')),
    url (r'^prompt/', 'prompt.search'),
    url (r'^participants/$', 'participants.search'),
    url (r'^participants/filter/$', 'participants.filter'),
    url (r'^participants/components/$', 'components.search'),
)
