from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts               import render

from browse.modelspackage.sites     import Site


@login_required
@permission_required('auth.can_view_sites')
def index (request):

    sites = Site.objects.all ()
    return render (request, 'browse/sites/index.html', {
        'sites': sites
    })


