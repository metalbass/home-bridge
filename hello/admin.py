from django.apps import apps
from django.contrib import admin

from .models import *  # Import all models so they can be added to the admin panel

for model in apps.get_app_config('hello').get_models():
    if not admin.site.is_registered(model):
        admin.site.register(model)
