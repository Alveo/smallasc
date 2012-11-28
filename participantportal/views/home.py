from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template import RequestContext

@login_required
def index (request):
  return render_to_response ('home.html', RequestContext (request))