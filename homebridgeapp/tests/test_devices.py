from django.test import TestCase

from ..models.devices import Device, Blind


class BlindTests(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.blind1 = Blind.objects.create(id='456', name='blind1')

    def test_get_description(self):
        expected_result = {
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

        self.assertDictEqual(self.blind1.get_description(), expected_result)

    def test_get_status(self):
        expected_result = {
            'online': True,
            'openPercent': 0
        }

        self.assertDictEqual(self.blind1.get_query_status(), expected_result)

    def test_execute_open_close_command(self):
        expected_result = {
            'ids': ['456'],
            'status': 'SUCCESS',
            'states': {
                'openPercent': 100,
                'online': True
            }
        }

        result = self.blind1.execute_command(Device.Command.OPEN_CLOSE, {'openPercent': 100})

        self.assertDictEqual(result, expected_result)
