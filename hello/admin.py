from django.contrib import admin
from django.apps import apps
from .models import *

admin.site.register(apps.get_app_config('hello').get_models())
