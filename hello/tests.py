import json

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from .models.device import *
from .views import api
from .views import index


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get("/")
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        self.assertEqual(response.status_code, 200)


class SyncTest(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.factory = RequestFactory()

    def test_details(self):
        request_data = {
            'requestId': 'ff36a3cc-ec34-11e6-b1a0-64510650abcf',
            'inputs': [{'intent': 'action.devices.SYNC'}]
        }

        device = Device(id='456', type=Device.Type.LIGHT, will_report_state=False, name='lamp1')
        device.save()

        device.traits.add(Device.Trait.ON_OFF)
        device.save()

        correct_result = {
            'requestId': 'ff36a3cc-ec34-11e6-b1a0-64510650abcf',
            'payload': {
                'agentUserId': '1836.15267389',
                'devices': [{
                    'id': '456',
                    'type': 'action.devices.types.LIGHT',
                    'traits': [
                        'action.devices.traits.OnOff',
                    ],
                    'name': {
                        'name': 'lamp1',
                    },
                    'willReportState': False,
                    # 'attributes': {
                    #     'temperatureMinK': 2000,
                    #     'temperatureMaxK': 6500
                    # },
                    # 'deviceInfo': {
                    #     'manufacturer': 'lights out inc.',
                    #     'model': 'hg11',
                    #     'hwVersion': '1.2',
                    #     'swVersion': '5.4'
                    # }
                }]
            }
        }

        request = self.factory.post('/api', data=json.dumps(request_data),
                                    content_type='application/json')

        dict_result = json.loads(api(request).content)

        self.assertDictEqual(dict_result, correct_result)
