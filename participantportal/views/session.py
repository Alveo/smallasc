from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from participantportal.forms.session import LoginForm, Password_Reset_Form


from browse.modelspackage.sparql_local_wrapper  import SparqlModel, SparqlManager
from browse.modelspackage.sites import Site
from browse.modelspackage.participants import *

def login_page(request):
  if request.method == 'POST':
    # When we receive the details we use our custom authenticator located in
    # the package participantportal.modelspackage.auth
    form = LoginForm(request.POST)
    if form.is_valid():
      # Our request should be routed to our custom authenticator
      # as configured in our AUTHENTICATION_BACKENDS field of settings.py
      user = authenticate(
        colour      = form.data['colour'], 
        animal      = form.data['animal'],
        birth_year  = form.cleaned_data['birth_year'],
        gender      = form.data['gender'])

      if user is not None:
        login(request, user)
        return HttpResponseRedirect ('/participantportal/')
      else:
        form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
  else:
    form = LoginForm()

  variables = RequestContext(request, {'form': form})
  return render_to_response('login.html', variables) 


def password_reset(request):
  
  if request.method == 'POST':
    form = Password_Reset_Form(request.POST)
    
    

    #if form.is_valid():
    
    if form.is_valid():
        # Our request should be routed to our custom authenticator
        # as configured in our AUTHENTICATION_BACKENDS field of settings.py
        '''
        custom_auth = CustomAuthBackend()
        #user = custom_auth.authenticate_password_reset(
        participant = custom_auth.authenticate_password_reset(
          site_label = form.data['pwd_site'],                
          birth_year  = form.data['pwd_birth_year'],
          gender      = form.data['pwd_gender']
          #mother_qual = form.cleaned_data['pwd_mother_qual'],


          )

        #if user is not None:
        if participant is not None:
          #login(request, user)
          #return HttpResponseRedirect ('/participantportal/')
          variables = RequestContext(request, {'name': participant.name } )
          return render_to_response ('password_reset_done.html', variables)
        else:
          form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
        '''

        site_label = form.data['pwd_site']

        highest_qual = form.data['pwd_highest_qual']
        highest_qual = highest_qual.lower()
        father_highest_qual = form.data['pwd_father_highest_qual']
        father_highest_qual = father_highest_qual.lower()
        mother_highest_qual = form.data['pwd_mother_highest_qual']
        mother_highest_qual = mother_highest_qual.lower()

        #print ('highest_qual : -------- ', highest_qual)
        #print ('father highest_qual : -------- ', father_highest_qual)

        #birth_year = int(form.data['pwd_birth_year'])
        #gender = form.data['pwd_gender']

        site = Site.objects.get(label=site_label)

        sparql = SparqlManager()

        sparql_results = sparql.query("""
                SELECT  ?part 
                where {
                    ?part rdf:type foaf:Person .
                    ?part austalk:recording_site <%s> .
                    ?part austalk:education_level ?education_level .
                    
                    ?part austalk:mother_education_level ?mother_education_level .

                    FILTER (lcase(str(?education_level)) = '%s' && lcase(str(?mother_education_level)) = '%s') .
                    OPTIONAL { ?part austalk:father_education_level ?father_education_level . FILTER ( lcase(str(?father_education_level)) = '%s') . }
                }""" % (site.identifier, highest_qual, mother_highest_qual, father_highest_qual))

        results = []
            
        for result in sparql_results["results"]["bindings"]:
            
            part = Participant (
                identifier          = result["part"]["value"]
                #gender              = result["gender"]["value"],
                #birth_year          = result["dob"]["value"]
            )

            results.append (part)

        #print "results --------------- ", results
        
        if len(results) != 0 :
          
          #variables = RequestContext(request, {'name': results[0].name, 'id' : results[0].id } )
          
          variables = RequestContext(request, {'results': results } )
          #return HttpResponseRedirect(reverse('/participantportal/reset/done', args=[results]))
          #return render_to_response ('/participantportal/reset/done', variables)
          return render_to_response ('password_reset_done.html', variables)
        else:
          form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())




  else:
    form = Password_Reset_Form()
  
  variables = RequestContext(request, {'form': form})

  return render_to_response('password_reset_form.html', variables) 


