def append_querystring_to_url(request, url):

    query_string = request.META["QUERY_STRING"] 
    
    if query_string: 
        url = "%s?%s" % (url, query_string)

    return url