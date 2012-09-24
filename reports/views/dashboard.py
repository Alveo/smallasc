from django.shortcuts import render_to_response
from reports.models import Poll

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('dashboard/index.html', {'latest_poll_list': latest_poll_list})