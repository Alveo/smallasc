
LOGIN_URL = "http://austalk.stevecassidy.net/login/?next=/"
AUTH_URL = "http://data.austalk.edu.au/"
AUTH_URL2 = "http://data.austalk.edu.au/MAUS/"
USERNAME = "demo"
PASSWORD = "austalk"


def getAuthenticatedOpener(url, username, password):
        """Returns an authenticated opener or None if login failed,
        This opener should be used for all subsequent requests to authenticated services"""
        import cookielib, urllib2, urllib
        from lxml import etree

        DEBUG = 1

        # create a cookie jar, build and install a cookie-enabled opener
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPHandler(debuglevel=DEBUG), \
                        urllib2.HTTPSHandler(debuglevel=DEBUG))
        urllib2.install_opener(opener)

        # obtain csrfmiddlewaretoken from the django login site 
        # (note that django sets csrfmiddlewaretoken as a cookie as well)
        parser = etree.HTMLParser(recover=True)
        doc = etree.fromstring(opener.open(LOGIN_URL).read(), parser=parser)
        csrfmiddlewaretokens = doc.xpath("//input[@name='csrfmiddlewaretoken']/@value")
        if len(csrfmiddlewaretokens) == 1:
                csrfmiddlewaretoken = csrfmiddlewaretokens[0]
        else:
                # TODO: handle error
                pass

        # create login POST data
        params = urllib.urlencode(dict(username=username, password=password, csrfmiddlewaretoken=csrfmiddlewaretoken))

        try:
                r = opener.open(LOGIN_URL, params)
        except urllib2.HTTPError as e:
                # TODO
                print e
                
        if r.geturl() == LOGIN_URL:
                print "login failed"
                return None
        else:
                return opener


if __name__ == "__main__":

        opener = getAuthenticatedOpener(LOGIN_URL, USERNAME, PASSWORD)

        if opener is not None:
                a = opener.open(AUTH_URL)
                print a.read()[:500]

                a = opener.open(AUTH_URL2)
                print a.read()[:500]

