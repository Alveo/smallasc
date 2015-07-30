from lettuce            import *
from lxml               import html
from django.test.client import Client
from nose.tools         import assert_equals


@step(r'If I set username to "(.*)" and password to "(.*)" following url "(.*)"')
def set_login_fields(step, username, password, url):

    response  = world.browser.post(url, { 'username': username, 'password': password }, follow = True)
    world.dom = html.fromstring(response.content)


@step(r'Then I see the alert "(.*)"')
def see_alert(step, alert_message):

    aside       = world.dom.cssselect('aside')[0]

    assert aside.text.strip() == alert_message
