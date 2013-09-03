from django.views.generic.base import TemplateView

from django.conf import settings


class StatsView(TemplateView):

    template_name = "statistics/p_report.html"

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        context['endpoint'] = settings.SPARQL_ENDPOINT
        return context