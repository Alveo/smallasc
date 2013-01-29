from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from participantportal.models import *

@login_required
@permission_required('auth.can_view_agreements')
def index (request):
    participants = UserProfile.objects.all()
    return render (request, 'browse/agreements/index.html', {'participants' : participants })

