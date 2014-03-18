from lettuce            import *
from lxml               import html
from django.test.client import Client
from nose.tools         import assert_equals


@step(r'Then I see the form "(.*)"')
def see_download_form(step, form_text):
    
    form        = world.dom.xpath("//form/legend")[0]

    assert form.text.strip() == form_text, \
        "form text '%s' does not equal expected text '%s'" % (form.text.strip(), form_text)


@step(r'I see that search result (\d) is "(.*)"')
def see_search_result(step, occurence, url):
    
    occurence   = int(occurence)
    link        = world.dom.xpath("//h2/a[%s]" % (occurence))[0]

    assert link.attrib['href'] == url, \
        "link href '%s' does not equal expected '%s'" % (link.attrib['href'], url)


@step(r'Then I see the partial prompt "(.*)"')
def see_partial_prompt(step, prompt_text_value):
    
    prompt        = world.dom.xpath("//tr[1]/th")[0]
    prompt_text   = world.dom.xpath("//tr[1]/td")[0]

    assert prompt.text_content() == "Prompt", "Expecting 'Prompt' label is result set."
    assert prompt_text.text_content() == prompt_text_value, \
        "Prompt text '%s' does not equal expected '%s'" % (prompt_text.text_content(), prompt_text_value)


@step(r'Then I should not see the field "(.*)"')
def not_see_field(step, field_name):
    
    field        = world.dom.xpath("//th[contains(text(), '%s')]" % (field_name))

    assert len(field) == 0, "Field '%s' is present" % (field)
