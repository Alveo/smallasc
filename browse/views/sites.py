from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator          import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts               import render
from smallasc.settings              import PAGE_SIZE

from browse.modelspackage.sites     import Site


@login_required
@permission_required('auth.can_view_sites')
def index(request):

    sites       = Site.objects.all()
    paginator   = Paginator(sites, PAGE_SIZE)

    page        = request.GET.get('page')
    try:
        sites_pages = paginator.page(page)
    except PageNotAnInteger:
        sites_pages = paginator.page(1)
    except EmptyPage:
        sites_pages = paginator.page(paginator.num_pages) 

    return render (request, 'browse/sites/index.html', {
        'request': request,
        'sites': sites_pages
    })


