from django.urls import path

from . import views
from .views import WebhookView

urlpatterns = [
    path('', views.index, name='root_path'),
    path('webhooks', views.webhooks, name='webhook'),
    path('app-uninstalled', WebhookView.as_view(), name='app-uninstalled'),
    path('test', views.test, name='test')
]
