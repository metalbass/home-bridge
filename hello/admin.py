from django.contrib import admin
from django.apps import apps

from .models import *  # Import all models so they can be added to the admin panel

admin.site.register(apps.get_app_config('hello').get_models())
