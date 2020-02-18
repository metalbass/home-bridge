from django.test import TestCase

from . import smarthome
from .models.device import Device


class SmartHomeTests(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_device_sync(self):
        device = Device(id='456', type=Device.Type.LIGHT, will_report_state=False, name='lamp1')
        device.traits.add(Device.Trait.ON_OFF)

        result = {
            'id': '456',
            'type': 'action.devices.types.LIGHT',
            'traits': [
                'action.devices.traits.OnOff',
            ],
            'name': {
                'name': 'lamp1',
            },
            'willReportState': False,
        }

        self.assertDictEqual(smarthome.device_sync(device), result)

    def test_device_query(self):
        device = Device(id='456', type=Device.Type.LIGHT, will_report_state=False, name='lamp1')
        device.traits.add(Device.Trait.ON_OFF)

        result = {
            'status': "SUCCESS",
            'online': True,
            'on': True
        }

        self.assertDictEqual(smarthome.device_query_status(device), result)
