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

    assert label.text == text, \
        "label text '%s' does not equal expected '%s'" % (label.text, text)


@step(r'I see that paragraph (\d) is "(.*)"')
def see_paragraph(step, occurence, text):
    
    occurence   = int(occurence)
    paragraph   = world.dom.xpath('//p[%s]' % (occurence))[0]

    assert paragraph.text_content().strip() == text, \
        "paragraph text '%s' does not equal expected '%s'" % (paragraph.text_content().strip(), text)


@step(r'Then I see the heading "(.*)"')
def see_heading(step, text):
    
    heading = world.dom.cssselect('h1')[0]

    assert heading.text.strip() == text, \
        "heading text '%s' does not equal expected '%s'" % (heading.text.strip(), text)


@step(r'I see that link (\d) is "(.*)"')
def see_link(step, occurence, url):
    
    occurence   = int(occurence)
    link        = world.dom.cssselect("a")[occurence - 1]

    assert link.attrib['href'] == url, \
        "link href '%s' does not equal expected '%s'" % (link.attrib['href'], url)


@step(r'After I login into the portal')
def login(step):

    world.browser.post('/login/', { 'username': 'joeblogs', 'password': 'password' }, follow = True)


@step(r'Then I see the button "(.*)"')
def see_button(step, text):
    
    button = world.dom.xpath('//input[@type="submit"]')[0]

    assert button.value == text


@step(r'Then I see a div for "(.*)"')
def see_div(step, name):

    div_element = world.dom.xpath('//div[@class="%s"]' % (name))

    assert len(div_element) == 1, \
        "Div element %s is missing or present too many times" % (name)