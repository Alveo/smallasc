from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts               import render

from baseapp.helpers                import generate_paginated_object
from browse.modelspackage.sites     import Site,SiteManager
from browse.modelspackage.sessions  import SessionManager

from baseapp.helpers import generate_breadcrumbs

@login_required
@permission_required('auth.can_view_sites')
def index(request):
    
    siteManager = SiteManager(client_json=request.session.get('client',None))
    sessionManager = SessionManager(client_json=request.session.get('client',None))

    sites = siteManager.all()
    
    counts = siteManager.all_site_and_session_counts()
    
    data = []
    for site in sites:
        res = counts.get(site.label,{1:"N/A",2:"N/A",3:"N/A",4:"N/A",})
        data.append((site,res['1'],res['2'],res['3'],res['4']))

    return render (request, 'browse/sites/index.html', {
        'request': request,
        'sites'  : data,
    })
