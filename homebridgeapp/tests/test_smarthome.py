from unittest.mock import MagicMock

from django.utils import timezone
from django.test import TestCase

from homebridgeapp import smarthome
from homebridgeapp.models.devices import Blind
from homebridgeapp.models.oauth import AccessToken


class SmartHomeTests(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.smartHome = smarthome.SmartHome()

        self.request_id = '1234ADDER'
        self.unauthorized_html_auth = 'Bearer UnauthorizedToken123'

        valid_token = 'ValidToken123'
        expired_token = 'ExpiredToken123'
        self.valid_html_auth = 'Bearer ' + valid_token
        self.expired_html_auth = 'Bearer ' + expired_token

        AccessToken.objects.create(token=valid_token)
        AccessToken.objects.create(token=expired_token, expiration=timezone.now())

    def test_authorized_process_fulfillment_calls_sync(self):
        mock = MagicMock(return_value={})
        self.smartHome._fulfillment_methods['action.devices.SYNC'] = mock

        self.smartHome.process_fulfillment({
            'requestId': self.request_id,
            'inputs': [{'intent': 'action.devices.SYNC'}]
        }, self.valid_html_auth)

        mock.assert_called_once()

    def test_unauthorized_process_fulfillment_fails_auth(self):
        request = {
            'requestId': self.request_id,
            'inputs': [{'intent': 'action.devices.SYNC'}]
        }

        expected_result = {
            'requestId': self.request_id,
            'payload': {'errorCode': 'authFailure'}
        }

        self.assertDictEqual(self.smartHome.process_fulfillment(request, self.unauthorized_html_auth), expected_result)

    def test_empty_auth_process_fulfillment_fails_auth(self):
        request = {
            'requestId': self.request_id,
            'inputs': [{'intent': 'action.devices.SYNC'}]
        }

        expected_result = {
            'requestId': self.request_id,
            'payload': {'errorCode': 'authFailure'}
        }

        self.assertDictEqual(self.smartHome.process_fulfillment(request, ''), expected_result)

    def test_expired_token_process_fulfillment_fails_auth(self):
        request = {
            'requestId': self.request_id,
            'inputs': [{'intent': 'action.devices.SYNC'}]
        }

        expected_result = {
            'requestId': self.request_id,
            'payload': {'errorCode': 'authExpired'}
        }

        self.assertDictEqual(self.smartHome.process_fulfillment(request, self.expired_html_auth), expected_result)

    def test_empty_sync(self):
        request = {
            'requestId': 'ff36a3cc-ec34-11e6-b1a0-64510650abcf',
            'inputs': [{
                'intent': 'action.devices.SYNC'
            }]
        }

        expected_result = {
            'agentUserId': '1836.15267389',
            'devices': []
        }

        self.assertDictEqual(self.smartHome.process_sync(request), expected_result)

    def test_blind_sync(self):
        request = {
            'requestId': 'ff36a3cc-ec34-11e6-b1a0-64510650abcf',
            'inputs': [{
                'intent': 'action.devices.SYNC'
            }]
        }

        blind = Blind(id='456', will_report_state=False, name='blind1')
        blind.save()

        expected_result = {
            'agentUserId': '1836.15267389',
            'devices': [{
                'id': '456',
                'type': 'action.devices.types.BLINDS',
                'traits': [
                    'action.devices.traits.OpenClose'
                ],
                'attributes': {
                    'openDirection': ['UP', 'DOWN']
                },
                'name': {
                    'name': 'blind1',
                },
                'willReportState': False
            }]
        }

        self.assertDictEqual(self.smartHome.process_sync(request), expected_result)

    def test_blind_query_fulfillment(self):
        request = {
            'requestId': 'ff36a3cc-ec34-11e6-b1a0-64510650abcf',
            'inputs': [{
                'intent': 'action.devices.QUERY',
                'payload': {
                    'devices': [
                        {'id': '456'}
                    ]
                }
            }]
        }

        blind = Blind(id='456', will_report_state=False, name='blind1', open_percent=40)
        blind.save()

        expected_result = {
            'devices': {
                '456': {
                    'online': True,
                    'openPercent': 40,
                }
            }
        }

        self.assertDictEqual(self.smartHome.process_query(request), expected_result)

    def test_execute_open_blind(self):
        request = {
            'requestId': 'ff36a3cc-ec34-11e6-b1a0-64510650abcf',
            'inputs': [{
                'intent': 'action.devices.EXECUTE',
                'payload': {
                    'commands': [{
                        'devices': [{'id': '123'}],
                        'execution': [{
                            'command': 'action.devices.commands.OpenClose',
                            'params': {
                                'openPercent': 100
                            }
                        }]
                    }]
                }
            }]
        }

        Blind.objects.create(id='123', name='blind1')

        expected_result = {
            'commands': [{
                'ids': ['123'],
                'status': 'SUCCESS',
                'states': {
                    'openPercent': 100,
                    'online': True
                }
            }]
        }

        result = self.smartHome.process_execute(request)

        self.assertDictEqual(result, expected_result)
        self.assertEquals(Blind.objects.get(id='123').open_percent, 100)
