from django.test import TestCase

from . import smarthome
from .models.devices import Device, Blind, Bed


class DeviceTests(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_all_devices_return_blind_type(self):
        device = Blind(id='123', will_report_state=False, name='blind1')
        device.save()

        self.assertIsInstance(Device.get_all_devices()[0], Blind)

    def test_get_all_devices_can_call_abstract_method(self):
        device = Blind(id='123', will_report_state=False, name='blind1')
        device.save()

        self.assertEqual(Device.get_all_devices()[0].get_type(), Device.Type.BLINDS)

    def test_get_all_devices_set_of_types(self):
        device = Blind(id='123', will_report_state=False, name='blind1')
        device.save()

        device = Bed(id='456', will_report_state=False, name='bed1')
        device.save()

        types = {d.get_type() for d in Device.get_all_devices()}

        self.assertSetEqual({Device.Type.BLINDS, Device.Type.BED}, types)


class BlindTests(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_get_description(self):
        device = Blind(id='456', will_report_state=False, name='blind1')

        result = {
            'id': '456',
            'type': 'action.devices.types.BLINDS',
            'traits': [
                'action.devices.traits.OpenClose',
            ],
            'attributes': {
                'openDirection': [
                    'UP',
                    'DOWN'
                ]},
            'name': {
                'name': 'blind1',
            },
            'willReportState': False,
        }

        self.assertDictEqual(device.get_description(), result)

    def test_get_status(self):
        device = Blind(id='456', will_report_state=False, name='blind1')

        result = {
            'online': True,
            'openPercent': 0
        }

        self.assertDictEqual(device.get_query_status(), result)


class SmartHomeTests(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_empty_sync_fulfillment(self):
        request = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "inputs": [{
                "intent": "action.devices.SYNC"
            }]
        }

        result = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "agentUserId": "1836.15267389",
                "devices": []
            }
        }

        self.assertDictEqual(smarthome.process_fulfillment(request), result)

    def test_blind_sync_fulfillment(self):
        request = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "inputs": [{
                "intent": "action.devices.SYNC"
            }]
        }

        blind = Blind(id='456', will_report_state=False, name='blind1')
        blind.save()

        result = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "agentUserId": "1836.15267389",
                "devices": [{
                    "id": "456",
                    "type": "action.devices.types.BLINDS",
                    "traits": [
                        "action.devices.traits.OpenClose"
                    ],
                    "attributes": {
                        'openDirection': ['UP', 'DOWN']
                    },
                    "name": {
                        "name": "blind1",
                    },
                    "willReportState": False
                }]
            }
        }

        self.assertDictEqual(smarthome.process_fulfillment(request), result)

    def test_blind_query_fulfillment(self):
        request = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "inputs": [{
                "intent": "action.devices.QUERY",
                "payload": {
                    "devices": [
                        {"id": "456"}
                    ]
                }
            }]
        }

        blind = Blind(id='456', will_report_state=False, name='blind1', open_percent=40)
        blind.save()

        result = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "devices": {
                    "456": {
                        "online": True,
                        "openPercent": 40,
                    }
                }
            }
        }

        self.assertDictEqual(smarthome.process_fulfillment(request), result)
