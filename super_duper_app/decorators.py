import json
from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.apps import apps

import hashlib, base64, hmac
import shopify
import logging

logger = logging.getLogger('debug')


class HttpResponseMethodNotAllowed(HttpResponse):
    status_code = 405

def domain_is_valid(domain):
    if domain is None:
        return False
    return len(domain) > 0
def get_hmac(body, secret):
    """
    Calculate the HMAC value of the given request body and secret as per Shopify's documentation for Webhook requests.
    See: http://docs.shopify.com/api/tutorials/using-webhooks#verify-webhook
    """
    hash = hmac.new(secret.encode('utf-8'), body, hashlib.sha256)
    return base64.b64encode(hash.digest()).decode()
def hmac_is_valid(body, secret, hmac_to_verify):
    return get_hmac(body, secret) == hmac_to_verify


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
        if not hmac_is_valid(request.body, apps.get_app_config('shopify_app').SHOPIFY_API_SECRET, hmac):
            logger.warning("Hmac verification failed.")
            return HttpResponseForbidden()

        # Otherwise, set properties on the request object and return.
        request.webhook_topic   = topic
        request.webhook_data    = data
        request.webhook_domain  = domain
        return f(request, *args, **kwargs)

    return wrapper