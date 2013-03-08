from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.views import login as django_login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import datetime
import urlparse


@csrf_exempt
def is_valid_session(request):
        print 'bla'
        print request.POST.get('sessionid')
        if request.method == 'POST':
                session_key = request.POST.get('sessionid')
                s = get_object_or_404(Session, session_key=session_key, expire_date__gt=datetime.datetime.now())
                # just to make sure this is not an anonymous session
                uid = s.get_decoded().get('_auth_user_id')
                user = get_object_or_404(User, pk=uid)

                return HttpResponse('OK')
        else:
                return HttpResponseNotAllowed(['POST'])


def login(request):
        if request.method == 'POST' or request.user.is_authenticated():
                if not request.user.is_authenticated():
                        l = django_login(request)

                        # authentication failed
                        if not request.user.is_authenticated():
                                return l

                next = request.REQUEST.get('next', settings.LOGIN_REDIRECT_URL)
                next_host = urlparse.urlparse(next).netloc
                next_scheme = urlparse.urlparse(next).scheme

                # ??? which server is the user trying to log in?
                # let's keep him here :)
                if next_host == "":
                        return HttpResponseRedirect(next)

                context = { 'sso_login_url' : '%s://%s/sso/login/' % (next_scheme, next_host),
                            'login_site' : next_host,
                            'next' : next,
                            'sessionid' : request.session.session_key,
                }
                return render_to_response("sso/authenticated.html", context)

        else:
                return django_login(request)


