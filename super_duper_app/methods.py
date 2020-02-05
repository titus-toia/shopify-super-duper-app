#Todo: Use a proper service layer later on
import shopify
import logging
import json

from datetime import timedelta
from django.utils import timezone
from django.apps import apps
from django.conf import settings

logger = logging.getLogger('debug')

#Requires login
def subscribe_webhooks(sender, **kwargs):
    hook = shopify.Webhook()
    hook.topic = "app/uninstalled"
    hook.address = settings.BASE_URL_SSL + "app-uninstalled"
    hook.format = "json"
    hook.save()
    if(hook.errors):
        logger.error(hook.errors.full_messages())

def queue_welcome_sms(sender, **kwargs):
    from shopify_app.models import Task

    # shop = shopify.Shop.current()
    # user = shopify.User.current()

    # data = {
    #     'phone': user.phone or '+40761349197',
    #     'firstname': user.first_name,
    #     'storename': shop.name,
    #     'customer_count': len(shopify.Customer.find())
    # }
    
    # task = Task(method="send_welcome_email",
    #     data=json.dumps(data),
    #     scheduled_on=timezone.now() + timedelta(minutes=5))
    # task.save()