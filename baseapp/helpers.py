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


def generate_breadcrumbs(request, site=None):
	url = request.path
	url_parts = url.split('/')
	url_parts = filter(None, url_parts)
	breadcrumbs = '<ul class="breadcrumb">'

	label = ''
	i = 0
	while i < len(url_parts):
		#for i in range(2,len(url_parts)):
		combined_url= ('/').join(url_parts[0:i+1])
		if url_parts[0]== 'browse' and i == 0:
			label = 'All Sites'
		elif url_parts[0] == 'participantportal' and i == 0:
			label = 'Participant Portal'
			i = 2
		elif i==1:
			if site:
				label = site.name
			else:
				label = url_parts[i].capitalize()
		elif i== 2:
			label = "Speaker " + url_parts[2]
		elif i== 3:
			label = "Session " + url_parts[3]
		else:
			label = url_parts[i-1]
		
		i = i + 1	
		breadcrumbs += '''<li><a href="/'''+ combined_url + '''">''' + label + ''' </a></li>'''


	breadcrumbs += '</ul>'
		
	#print ('printing request url')
	#print (breadcrumbs)
	return breadcrumbs