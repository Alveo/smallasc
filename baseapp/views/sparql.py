from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseBadRequest
from django import forms
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from SPARQLWrapper import SPARQLWrapper

class SparqlForm(forms.Form):
    
    query = forms.CharField(label='SPARQL Query', max_length=5000, widget=forms.Textarea)
    # not supporting these fields
    # output
    # default-graph-uri
    # named-graph-uri


@csrf_exempt
@login_required
def sparql_endpoint(request): 
    """Implement a SPARQL endpoint to query the RDF triple store"""
    
    if request.method == 'GET': 
        form = SparqlForm(request.GET)

        if form.is_valid():  
            queryString = form.cleaned_data['query']
            outputFormat = "json"
            
            # run the query
            try:
                sparql = SPARQLWrapper (settings.SPARQL_ENDPOINT, returnFormat=outputFormat)
                
                sparql.setQuery(queryString)
                result = sparql.query()
                
                # create a Django response passing the result which will be 
                # treated as an iterator
                return HttpResponse(result, content_type=result.info()['content-type'])
                  
            except Exception as e:
                # 400 Bad Request
                return HttpResponseBadRequest("Bad Request:" + str(e))
            
    else:
        form = SparqlForm()
            
    return render(request, 'sparql.html', {
        'form': form,
    })
    
    

