from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from participantportal.models import *
from participantportal.settings import *

@login_required(login_url = PP_LOGIN_URL)
def index (request):
    participants = UserProfile.objects.all()
    return render (request, 'participants/index.html', {'participants' : participants })
