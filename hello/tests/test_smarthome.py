from unittest.mock import MagicMock

from django.test import TestCase

from hello import smarthome
from hello.models.devices import Blind


class SmartHomeTests(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.smartHome = smarthome.SmartHome()

    def test_process_fulfillment_sync(self):
        mock = MagicMock(return_value={})
        self.smartHome._fulfillment_methods['action.devices.SYNC'] = mock

        self.smartHome.process_fulfillment({"inputs": [{"intent": "action.devices.SYNC"}]})

        mock.assert_called_once()

    def test_process_fulfillment_query(self):
        mock = MagicMock(return_value={})
        self.smartHome._fulfillment_methods['action.devices.QUERY'] = mock

        self.smartHome.process_fulfillment({"inputs": [{"intent": "action.devices.QUERY"}]})

        mock.assert_called_once()

    def test_process_fulfillment_execute(self):
        mock = MagicMock(return_value={})
        self.smartHome._fulfillment_methods['action.devices.EXECUTE'] = mock

        self.smartHome.process_fulfillment({"inputs": [{"intent": "action.devices.EXECUTE"}]})

        mock.assert_called_once()

    def test_process_fulfillment_disconnect(self):
        mock = MagicMock(return_value={})
        self.smartHome._fulfillment_methods['action.devices.DISCONNECT'] = mock

        self.smartHome.process_fulfillment({"inputs": [{"intent": "action.devices.DISCONNECT"}]})

        mock.assert_called_once()

    def test_empty_sync(self):
        request = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "inputs": [{
                "intent": "action.devices.SYNC"
            }]
        }

        expected_result = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "agentUserId": "1836.15267389",
                "devices": []
            }
        }

        self.assertDictEqual(self.smartHome.process_sync(request), expected_result)

    def test_blind_sync(self):
        request = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "inputs": [{
                "intent": "action.devices.SYNC"
            }]
        }

        blind = Blind(id='456', will_report_state=False, name='blind1')
        blind.save()

        expected_result = {
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

        self.assertDictEqual(self.smartHome.process_sync(request), expected_result)

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

        expected_result = {
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

        self.assertDictEqual(self.smartHome.process_query(request), expected_result)

    def test_execute_open_blind(self):
        request = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "inputs": [{
                "intent": "action.devices.EXECUTE",
                "payload": {
                    "commands": [{
                        "devices": [{"id": "123"}],
                        "execution": [{
                            "command": "action.devices.commands.OpenClose",
                            "params": {
                                "openPercent": 100
                            }
                        }]
                    }]
                }
            }]
        }

        Blind.objects.create(id='123', name='blind1')

        expected_result = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "payload": {
                "commands": [
                    {
                        "ids": ["123"],
                        "status": "SUCCESS",
                        "states": {
                            "openPercent": 100,
                            "online": True
                        }
                    }
                ]
            }
        }

        result = self.smartHome.process_execute(request)

        self.assertDictEqual(result, expected_result)
        self.assertEquals(Blind.objects.get(id='123').open_percent, 100)
