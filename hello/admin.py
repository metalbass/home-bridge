from django.apps import apps
from django.contrib import admin

from .models import *  # Import all models so they can be added to the admin panel


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', '_traits', 'will_report_state']

    def _traits(self, obj: device.Device):
        return '{%s}' % (', '.join([trait.name for trait in obj.traits]))


admin.site.register(device.Device, DeviceAdmin)

for model in apps.get_app_config('hello').get_models():
    if not admin.site.is_registered(model):
        admin.site.register(model)
