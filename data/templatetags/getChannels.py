
from django import template

from data import choices


register = template.Library()

@register.assignment_tag
def getChannels():
        return choices.CHANNELS

