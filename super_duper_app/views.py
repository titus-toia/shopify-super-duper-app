
from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import shopify
from shopify_app.decorators import shop_login_required
from .decorators import webhook


import logging
logger = logging.getLogger('debug')

@shop_login_required
def index(request):
    products = shopify.Product.find(limit=3)
    orders = shopify.Order.find(limit=3, order="created_at DESC")
    return render(request, 'base/index.html', {'products': products, 'orders': orders})
@shop_login_required
def webhooks(request):
    webhooks = shopify.Webhook.find()
    return render(request, 'base/webhooks.html', {'webhooks': webhooks})
@shop_login_required
def uninstalled(request):
    pass

class WebhookView(View):
    @csrf_exempt
    @webhook
    @shop_login_required
    def post(self, request, *args, **kwargs):
        topic = request.webhook_topic
        logger.info("Webhook hit " + topic)
        """
        Receive a webhook POST request.
        """

        # Convert the topic to a signal name and trigger it.
        # signal_name = get_signal_name_for_topic(request.webhook_topic)
        # try:
        #     signals.webhook_received.send_robust(self, domain = request.webhook_domain, topic = request.webhook_topic, data = request.webhook_data)
        #     getattr(signals, signal_name).send_robust(self, domain = request.webhook_domain, topic = request.webhook_topic, data = request.webhook_data)
        # except AttributeError:
        #     return HttpResponseBadRequest()

        # All good, return a 200.
        return HttpResponse('OK')