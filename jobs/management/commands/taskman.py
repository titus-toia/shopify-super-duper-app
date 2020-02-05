
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
        tasks = Task.objects.filter(
            executed=False,
            retry__gt=0,
            scheduled_on__lte=timezone.now()
        )
        print(str(tasks.count()) + " tasks to execute.")
        
        for task in tasks:
            try:
                self.dispatch(task.method, task, json.loads(task.data))
                task.executed = True
                task.save()
            except:
                task.retry -= 1
                task.save()   

    def dispatch(self, method, task, data):
        handler = getattr(self, method)
        if callable(handler):
            handler(task, data)

    def send_welcome_email(self, task, data):
        body = f"Hi {data['firstname']}, it’s great to see {data['storename']} installed with our app. {data['customer_count']} people will love it."
        self.twclient.messages.create(
            to=data.get('phone'), 
            from_="+12018347169",
            body=body)

    def _create_dummy_task(self):
        data = {
            'phone': '+40761349197',
            'firstname': 'Titus',
            'storename': 'Titon Gymbox',
            'customer_count': 5
        }
        scheduled_on = timezone.now() + timedelta(minutes=-5)
        task = Task(method="send_welcome_email", data=json.dumps(data), scheduled_on=scheduled_on)
        task.save()


