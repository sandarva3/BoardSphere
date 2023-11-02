#TO GET THE PROFILE PICTURE FROM gravatar.com:
'''

import hashlib
from urllib.parse import urlencode

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def gravatar(user):
    email = user.email.lower().encode('utf-8')
    default = 'mm'
    size = 256
    url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
        md5=hashlib.md5(email).hexdigest(),
        params=urlencode({'d': default, 's': str(size)})
    )
    return url

'''
# AFTER THIS WE ONLY NEED TO LOAD GRAVATAR ON TEMPLATE PAGE({% load gravatar %}) AND while using the syntax is, eg: {{post.created_by|gravatar}}