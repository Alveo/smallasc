from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from participantportal.settings import *
from participantportal.models import *

@login_required(login_url = PP_LOGIN_URL)
def index (request):
  if request.method == 'POST':
    if u'agreementstatus_id' in request.POST:
      # The form specifies this field explicitly, therefore it is okay to access
      # the value directly using the key
      agreementstatus_id = request.POST[u'agreementstatus_id']
      agreementstatus = AgreementStatus.objects.get(id = agreementstatus_id)
      if not agreementstatus is None:
        agreementstatus.accept(date.today())
        agreementstatus.save()

  agreement_status_set = request.user.userprofile.agreementstatus_set.all()
  return render (request, 'termsandconditions.html', { 'agreement_status_set': agreement_status_set })