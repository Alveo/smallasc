from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.flatpages.models import FlatPage

#@login_required
#@permission_required('auth.can_view_dashboard')
def index (request):
    
    pages = FlatPage.objects.filter(url='/')
    
    if pages:
        page = pages[0]
    else:
        page = None
    
    return render (request, 'index.html', {
		'page' : page
		})
