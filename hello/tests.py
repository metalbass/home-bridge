from django.test import TestCase, RequestFactory

from .models.device import *


class DeviceTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_to_dict(self):
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

        self.assertDictEqual(device.to_dict(), result)
