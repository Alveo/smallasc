from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def smallascdataEndpoint():
            return settings.SMALLASCDATA_ENDPOINT

