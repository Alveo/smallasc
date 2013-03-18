from lettuce            import *
from lxml               import html
from django.test.client import Client
from nose.tools         import assert_equals


@before.all
def set_browser():
    
    world.browser = Client()


@step(r'I access the url "(.*)"')
def access_url(step, url):
    
    response    = world.browser.get(url)
    world.dom   = html.fromstring(response.content)


@step(r'I see that label (\d) is "(.*)"')
def see_label(step, occurence, text):
    
    occurence   = int(occurence)
    label       = world.dom.cssselect('label')[occurence - 1]

    assert label.text == text


@step(r'Then I see the heading "(.*)"')
def see_heading(step, text):
    
    heading = world.dom.cssselect('h1')[0]

    assert heading.text.strip() == text


@step(r'I see that link (\d) is "(.*)"')
def see_link(step, occurence, url):
    
    occurence   = int(occurence)
    link        = world.dom.cssselect("a")[occurence - 1]

    assert link.attrib['href'] == url


@step(r'After I login into the portal')
def login(step):

    world.browser.post('/login/', { 'username': 'joeblogs', 'password': 'password' }, follow = True)