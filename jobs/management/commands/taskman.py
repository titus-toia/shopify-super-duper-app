
import json
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from shopify_app.models import Task
from django.utils import timezone
from datetime import timedelta
from twilio.rest import Client


class Command(BaseCommand):
    def __init__(self):
        app_config = apps.get_app_config('super_duper_app')
        sid = app_config.twilio_account_sid
        token = app_config.twilio_auth_token
        self.twclient = Client(sid, token)

    def handle(self, *args, **options):
        print(timezone.now())
        tasks = Task.objects.filter(
            executed=False,
            retry__gt=0,
            scheduled_on__lte=timezone.now()
        )
        print(str(tasks.count()) + " tasks to execute.")
        executed = 0
        
        for task in tasks:
            try:
                self.dispatch(task.method, task, json.loads(task.data))
                task.executed = True
                task.save()
                executed += 1
            except:
                task.retry -= 1
                task.save()
        print("Of which, " + str(executed) + " tasks executed.")

    def dispatch(self, method, task, data):
        handler = getattr(self, method)
        if callable(handler):
            return handler(task, data)
        raise ValueError("No such method exists")

    def send_welcome_email(self, task, data):
        body = f"Hi {data['firstname']}, it’s great to see {data['storename']} installed with our app. {data['customer_count']} people will love it."
        self.twclient.messages.create(
            to=data.get('phone'), 
            from_="+12018347169",
            body=body)


