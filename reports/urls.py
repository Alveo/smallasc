from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from reports.models import Poll

urlpatterns = patterns('reports.views',
    # Reports
    url (r'^$',
            ListView.as_view (
                queryset = Poll.objects.order_by ('-pub_date')[:5],
                context_object_name = 'latest_poll_list',
                template_name = 'dashboard/index.html'
            )
        ),
    url (r'^(?P<pk>\d+)/$',
            DetailView.as_view (
                model = Poll,
                template_name = 'dashboard/detail.html'
            )
        ),
    # url (r'^$', 'dashboard.index'),
    #url(r'^(?P<report_id>\d+)/$', 'dashboard.detail'),
    url(r'^(?P<report_id>\d+)/results/$', 'dashboard.results'),
    url(r'^(?P<report_id>\d+)/vote/$', 'dashboard.vote'),
)
