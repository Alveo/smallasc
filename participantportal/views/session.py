from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.utils import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
from participantportal.forms.session import LoginForm, ColourAnimalHelperForm

  
from browse.modelspackage.sparql_local_wrapper  import SparqlModel, SparqlManager
from browse.modelspackage.sites import SiteManager
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
                request.session['client'] = settings.PPCLIENT
                return HttpResponseRedirect ('/participantportal/')
            else:
                form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
    else:
        form = LoginForm()
    
    return render(request,'login.html', {'form': form}) 

# view to display the possible Colour-Animal Combination after the user answers a couple of questions
def password_reset(request):
  
    if request.method == 'POST':
        form = ColourAnimalHelperForm(request.POST)
        
        
        if form.is_valid():
            # Create a SPARQL Query to retrieve possible results based on the answers
            
            siteManager = SiteManager(client_json=request.session.get('client',None))
            
            # Get the site object from site_label (get function needs a label parameter)
            site_label = form.data['pwd_site'] 
            site = siteManager.get(label=site_label)
            
            query = '?part austalk:recording_site <%s> .\n' % site.identifier
            
            # Grab all the form data and convert them to lower case
            # in order to compare the result of SPARQL Query
            
            if form.data['pwd_highest_qual'] != 'None':
                value = form.data['pwd_highest_qual']
                query += "?part austalk:education_level '%s' .\n" % value
                
            
            if form.data['pwd_father_highest_qual'] != 'None':
                value = form.data['pwd_father_highest_qual']
                query += "?part austalk:father_education_level '%s' .\n" % value 
            
            
            if form.data['pwd_mother_highest_qual'] != 'None':
                value = form.data['pwd_mother_highest_qual']
                query += "?part austalk:mother_education_level '%s' .\n" % value 
            
            sparql = SparqlManager()
            
            sparql_results = sparql.query("""
                    SELECT  ?part 
                    where {
                        ?part rdf:type foaf:Person . 
                        %s
                    }""" % query)
            
            results = []
        
        # Bind the result from SPARQL query into a list - results            
        for result in sparql_results["results"]["bindings"]:
            
            part = Participant (
                identifier          = result["part"]["value"]
                
            )
            
            results.append (part)
        
        # return the results to the template for displaying to the user
        return render(request,'colour_animal_helper_done.html', {'results': results }) 
    
    else:
        form = ColourAnimalHelperForm()
    
    return render(request, 'colour_animal_helper_form.html', {'form': form}) 


