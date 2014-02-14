from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.views import login as django_login
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404

from sso.models import TSession

import datetime
import urlparse
import hashlib
import logging
# Get an instance of a logger
logger = logging.getLogger('django')


@csrf_exempt
def is_valid_session(request):
        if request.method == 'POST':
                session_key = request.POST.get('sessionid')
                
                logger.debug("Looking up sessionid: %s" % (session_key,))
                
                s = get_object_or_404(Session, session_key=session_key, expire_date__gt=timezone.now())
                # just to make sure this is not an anonymous session
                uid = s.get_decoded().get('_auth_user_id')
                user = get_object_or_404(User, pk=uid)

                return HttpResponse('OK')
        else:
                return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def is_valid_tsession(request):
        if request.method == 'POST':
                tsession_key = request.POST.get('sessionid')
                
                logger.debug("Looking up tsessionid: %s" % (tsession_key,))
                
                ss = TSession.objects.filter(tsession_key__exact=tsession_key, expire_date__gt=timezone.now())
                if ss.count() == 0:
                    raise Http404
                elif ss.count() > 1:
                    # too many sessions, remove all but the first one
                    for s in ss[1:]:
                        s.delete()
                    s = ss[0]
                else:
                    s = ss[0]

                return HttpResponse(s.session_key)
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
                parsed_next = urlparse.urlparse(next) 

                # ??? which server is the user trying to log in?
                # let's keep him here :)
                if parsed_next.netloc == "":
                        return HttpResponseRedirect(next)

                # create a temporary session key (expires in 20s)
                tsession = hashlib.md5(request.session.session_key).hexdigest()
                TSession.objects.get_or_create(user=request.user, session_key=request.session.session_key, \
                      defaults={'expire_date' : timezone.now() + datetime.timedelta(seconds=20), 
                                'tsession_key' : tsession, })
                
                return HttpResponseRedirect('%s://%s/sso/login/?tsessionid=%s&next=%s' % (parsed_next.scheme, parsed_next.netloc, tsession, parsed_next.path))
        else:
                return django_login(request)


@login_required
def test_embedded(request):
        return render_to_response("sso/test_embedded.html")

