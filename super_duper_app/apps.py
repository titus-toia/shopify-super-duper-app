from django.apps import AppConfig
from shopify_app.signals import app_installed, app_login
from .methods import queue_welcome_sms, subscribe_webhooks

class SuperDuperAppConfig(AppConfig):
    name = 'super_duper_app'
    twilio_account_sid = 'AC6284c2dd5fcb7ca3d102aff51f93c8cc'
    twilio_auth_token = '61d9c7ab58a1a7a4b061bcfbf2c9edb6'

    def ready(self):
        #Django is run in separate threads so we need to ensure this is registered only once
        app_installed.connect(queue_welcome_sms, dispatch_uid="queue_welcome_sms")
        app_login.connect(subscribe_webhooks, dispatch_uid="subscribe_webhooks")