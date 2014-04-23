from django.core.paginator      import Paginator, EmptyPage, PageNotAnInteger
from smallasc.settings          import PAGE_SIZE

from browse.modelspackage.sites import Site

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


def generate_breadcrumbs(request, site):
	url = request.path
	url_parts = url.split('/')
	breadcrumbs = '<ul class="breadcrumb">'

	
	label = ''
	for i in range(2,len(url_parts)):
		combined_url= ('/').join(url_parts[0:i])
		if url_parts[1]== 'browse' and  i == 2:
			label = 'All Sites'
		elif url_parts[1] == 'participantportal' and i == 2:
			label = 'Participant Portal'
		elif i==3:
			label = site.name
		elif i== 4:
			label = "Speaker " + url_parts[3]
		elif i== 5:
			label = "Session " + url_parts[4]
		else:
			label = url_parts[i-1]
			
		breadcrumbs += '''<li><a href="'''+ combined_url + '''">''' + label + ''' </a></li>
					

		'''


	breadcrumbs += '</ul>'
		
	print ('printing request url')
	print (breadcrumbs)
	return breadcrumbs