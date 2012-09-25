from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from reports.models import Choice, Poll

def index (request):
    latest_poll_list = Poll.objects.all ().order_by ('-pub_date')[:5]
    return render_to_response ('dashboard/index.html', {'latest_poll_list': latest_poll_list})


def detail (request, report_id):
    p = get_object_or_404 (Poll, pk = report_id)
    return render_to_response ('dashboard/detail.html', {'poll': p}, 
                                context_instance = RequestContext (request))


def results(request, report_id):
    p = get_object_or_404 (Poll, pk=report_id)
    return render_to_response ('dashboard/results.html', {'poll': p})

def vote(request, report_id):
    p = get_object_or_404 (Poll, pk = report_id)
    try:
        selected_choice = p.choice_set.get (pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render_to_response ('dashboard/detail.html', {
                'poll': p,
                'error_message': "You didn't select a choice.",
            }, context_instance = RequestContext (request)
            )
    else:
        selected_choice.votes += 1
        selected_choice.save ()
        return HttpResponseRedirect (reverse ('reports.views.dashboard.results', args = (p.id,)))
