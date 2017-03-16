from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts               import render

from baseapp.helpers                import generate_paginated_object
from browse.modelspackage.sites     import Site,SiteManager

from baseapp.helpers import generate_breadcrumbs

@login_required
@permission_required('auth.can_view_sites')
def index(request):
    
    siteManager = SiteManager(client=request.session.get('client',None))

    sites = siteManager.all()

    return render (request, 'browse/sites/index.html', {
        'request': request,
        'sites'  : sites,
    })
