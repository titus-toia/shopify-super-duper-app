
from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

def uninstalled(request):
    pass

class WebhookView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(webhook)    
    def dispatch(self, request, *args, **kwargs):
        return super(WebhookView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        topic = request.webhook_topic

        if(topic != "app/uninstalled"):
            return HttpResponseBadRequest()
        
        logger.info("Webhook hit " + topic)


        return HttpResponse('OK')