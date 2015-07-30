from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from participantportal.forms.session import LoginForm, ColourAnimalHelperForm

  
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

# view to display the possible Colour-Animal Combination after the user answers a couple of questions
def password_reset(request):
  
  if request.method == 'POST':
    form = ColourAnimalHelperForm(request.POST)
    
    

    #if form.is_valid():
    
    if form.is_valid():
        # Create a SPARQL Query to retrieve possible results based on the answers

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

        # Get the site object from site_label (get function needs a label parameter)
        site_label = form.data['pwd_site'] 
        site = Site.objects.get(label=site_label)

        # Grab all the form data and convert them to lower case
        # in order to compare the result of SPARQL Query

        highest_qual = form.data['pwd_highest_qual']
        highest_qual = highest_qual.lower()
        father_highest_qual = form.data['pwd_father_highest_qual']
        father_highest_qual = father_highest_qual.lower()
        mother_highest_qual = form.data['pwd_mother_highest_qual']
        mother_highest_qual = mother_highest_qual.lower()

       
        # lcase in SPARQL Query converts the retrieved field into lower case
        # Father's education level is made optional because not all participants have Father's education level
        
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
        
        # Bind the result from SPARQL query into a list - results            
        for result in sparql_results["results"]["bindings"]:
            
            part = Participant (
                identifier          = result["part"]["value"]
                
            )

            results.append (part)

        print ('results of password recovery ---- ', results)
        # Check if there is any result based on the answers to the questions in the form
        if len(results) != 0 :
          variables = RequestContext(request, {'results': results } )
          # return the results to the template for displaying to the user
          return render_to_response ('colour_animal_helper_done.html', variables)
        else:
          form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())

  else:
    form = ColourAnimalHelperForm()
  
  variables = RequestContext(request, {'form': form})

  return render_to_response('colour_animal_helper_form.html', variables) 


