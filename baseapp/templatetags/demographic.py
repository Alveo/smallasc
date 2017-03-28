from django import template
from django.conf import settings
from browse.helpers import get_language_name
from browse.modelspackage.participants import ParticipantManager


register = template.Library()

@register.simple_tag
def language(url):
    return get_language_name("<"+url+">")


@register.simple_tag(takes_context=True)
def participant(context, id):
    request = context['request']
    participantManager = ParticipantManager(client_json=request.session.get('client',None))
    participant = participantManager.get(id)
    if not participant is None:
        return participant.get_name()
    else:
        return id
    