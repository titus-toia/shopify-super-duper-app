#Todo: Use a proper service layer later on
import shopify
import logging
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
    logger.info("APP HAS BEEN INSTALLED")
    logger.info("Should send SMS 5 minutes after")
    pass