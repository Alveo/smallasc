from django.http                    import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts               import render

from participantportal.models       import *
from baseapp.helpers import generate_breadcrumbs

@login_required
@permission_required('auth.can_view_agreements')
def index (request):
    
    participants = UserProfile.objects.all().order_by('-agreementstatus__has_agreed')
    breadcrumbs = generate_breadcrumbs(request)
    
    agreed = UserProfile.objects.filter(agreementstatus__has_agreed__exact=True)
    
    return render (request, 'browse/agreements/index.html', {
        'participants' : participants,
        'breadcrumbs' : breadcrumbs,
        'agreed' : agreed,
    })

