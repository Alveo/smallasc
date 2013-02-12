
from django import template
import jwt
from smallasc import settings


register = template.Library()

@register.filter
def createDataJson(item_ids, authenticated):
        json = '{ "media": [ ' + ",".join([ '"%s"' % item_id for item_id in item_ids ]) + ' ] }'
        if authenticated:
                return jwt.encode(json, settings.JWT_SECRET)
        else:
                return json

