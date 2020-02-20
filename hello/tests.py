import json

from django.test import TestCase

from . import smarthome
from .models.device import Device


class SmartHomeTests(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_device_sync(self):
        device = Device(id='456', type=Device.Type.BLINDS, will_report_state=False, name='lamp1')
        device.traits.add(Device.Trait.OPEN_CLOSE)
        device.attributes = '{"openDirection": ["UP","DOWN"]}'

        result = {
            'id': '456',
            'type': Device.Type.BLINDS,
            'traits': [
                Device.Trait.OPEN_CLOSE,
            ],
            'attributes': '{"openDirection": ["UP","DOWN"]}',
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
