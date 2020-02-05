import json
from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.conf import settings

import shopify
import logging

logger = logging.getLogger('debug')


class HttpResponseMethodNotAllowed(HttpResponse):
    status_code = 405

def domain_is_valid(domain):
    if domain is None:
        return False
    return len(domain) > 0

def webhook(f):
    """
    A view decorator that checks and validates a Shopify Webhook request.
    """
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        # Ensure the request is a POST request.
        if request.method != 'POST':
            return HttpResponseMethodNotAllowed()
        
        # Try to get required headers and decode the body of the request.
        try:
            topic   = request.META['HTTP_X_SHOPIFY_TOPIC']
            domain  = request.META['HTTP_X_SHOPIFY_SHOP_DOMAIN']
            hmac    = request.META['HTTP_X_SHOPIFY_HMAC_SHA256'] if 'HTTP_X_SHOPIFY_HMAC_SHA256' in request.META else None
            data    = json.loads(request.body.decode('utf-8'))
        except (KeyError, ValueError) as e:
            return HttpResponseBadRequest()

        # Verify the domain.
        if not domain_is_valid(domain):
            return HttpResponseBadRequest()

        # Verify the HMAC.
        if not shopify.Session.validate_hmac({'hmac': hmac}):
            logger.warning("Hmac verification failed.")
            return HttpResponseForbidden()

        # Otherwise, set properties on the request object and return.
        request.webhook_topic   = topic
        request.webhook_data    = data
        request.webhook_domain  = domain
        return f(request, *args, **kwargs)

    return wrapper