from django import template
from django.conf import settings
from browse.helpers import get_language_name
from browse.modelspackage.participants import Participant


register = template.Library()

@register.simple_tag
def language(url):
    return get_language_name("<"+url+">")


@register.simple_tag
def participant(id):
    participant = Participant.objects.get(id)
    if not participant is None:
        return participant.get_name()
    else:
        return id
    