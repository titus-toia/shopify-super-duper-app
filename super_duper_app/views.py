
from django.shortcuts import render
from django.views.generic import View
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

from django.apps import apps

import shopify

from shopify_app.decorators import shop_login_required
from shopify_app.models import Shop
from .decorators import webhook

app_config = apps.get_app_config('super_duper_app')

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
def test(request):
    from twilio.rest import Client
    sid = app_config.twilio_account_sid
    token = app_config.twilio_auth_token

    client = Client(sid, token)
    message = client.messages.create(
        to="+40761349197", 
        from_="+12018347169",
        body="Hello from Super Duper App")

    return HttpResponse('ok')


class WebhookView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(webhook)   
    def dispatch(self, request, *args, **kwargs):
        return super(WebhookView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        topic = request.webhook_topic
        data = request.webhook_data

        if(topic != "app/uninstalled"):
            return HttpResponseBadRequest()

        id = data.get('id')
        try:
            shop = Shop.objects.get(name = id)
            shop.installed = False
            shop.save()
            logger.info("Shop uninstalled: " + str(id))
        except ObjectDoesNotExist:
            logger.error("This shouldn't have happened: " + str(id))
        
        return HttpResponse('OK')