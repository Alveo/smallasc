from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
@permission_required('auth.can_view_dashboard')
def index (request):
	""" Render the dashboard """
	return render_to_response ('index.html', RequestContext (request))