from django.apps import AppConfig
import os


class ShopifyAppConfig(AppConfig):
    name = 'shopify_app'
    # Replace the API Key and Shared Secret with the one given for your
    # App by Shopify.
    #
    # To create an application, or find the API Key and Secret, visit:
    # - for private Apps:
    #     https://${YOUR_SHOP_NAME}.myshopify.com/admin/api
    # - for partner Apps:
    #     https://www.shopify.com/services/partners/api_clients
    #
    # You can ignore this file in git using the following command:
    #   git update-index --assume-unchanged shopify_settings.py
    SHOPIFY_API_KEY = 'SHOPIFY_API_KEY'
    SHOPIFY_API_SECRET = 'SHOPIFY_API_KEY'

    # API_VERSION specifies which api version that the app will communicate with
    SHOPIFY_API_VERSION = 'unstable'

    # See http://api.shopify.com/authentication.html for available scopes
    # to determine the permisssions your app will need.
    SHOPIFY_API_SCOPE = ['read_customers']
