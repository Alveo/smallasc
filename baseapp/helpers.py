from django.core.paginator      import Paginator, EmptyPage, PageNotAnInteger
from smallasc.settings          import PAGE_SIZE


def generate_paginated_object(request, collection):

    paginator   = Paginator(collection, PAGE_SIZE)
    page        = request.GET.get('page')

    try:
        paged_obj = paginator.page(page)
    except PageNotAnInteger:
        paged_obj = paginator.page(1)
    except EmptyPage:
        paged_obj = paginator.page(paginator.num_pages) 


    return paged_obj
