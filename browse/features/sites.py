from lettuce            import *
from lxml               import html
from django.test.client import Client
from nose.tools         import assert_equals


@step(r'Then I see that "(.*)" paragraph (\d) is "(.*)"')
def see_summary_paragraph(step, source, occurrence, paragraph):
    
    paragraph_text = world.dom.xpath("//p[%s]" % (occurrence))[0]

    assert paragraph in paragraph_text.text_content().strip(), \
        "paragraph text '%s' not in '%s'" % \
        (paragraph, paragraph_text.text_content().strip())