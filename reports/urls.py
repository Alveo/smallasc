from django.conf.urls import patterns, include, url

urlpatterns = patterns('reports.views',
    # Reports
    url (r'^$', 'dashboard.index'),
)
