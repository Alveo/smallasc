from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from django.conf import settings



class StatsView(TemplateView):
	#login_required = True
	template_name = "statistics/p_report.html"
	
	
	@method_decorator(login_required)
	@method_decorator(permission_required('auth.can_view_sites'))
	def dispatch(self, *args, **kwargs):
		return super(StatsView, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
	    context = super(StatsView, self).get_context_data(**kwargs)
	    context['endpoint'] = '/sparql/'
	    print('context -------- ', context)
	    return context 


