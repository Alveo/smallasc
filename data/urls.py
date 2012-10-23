from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('data.views',
    url(r'^$', 'download_redirect', name='download_redirect'),
    url(r'^download/(?P<h>.*)/', 'download', name='download'),
)

