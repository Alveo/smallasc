from django.shortcuts import render, render_to_response
from django.template import RequestContext

def index (request):
	""" Render the dashboard """
	return render_to_response ('index.html', RequestContext (request))