from django.utils import timezone

from .models.devices import Device
from .models.oauth import AccessToken


class SmartHome:
    def __init__(self):
        self._fulfillment_methods = {
            'action.devices.SYNC': SmartHome.process_sync,
            'action.devices.QUERY': SmartHome.process_query,
            'action.devices.EXECUTE': SmartHome.process_execute,
            'action.devices.DISCONNECT': SmartHome.process_disconnect,
        }

    def process_fulfillment(self, request: dict, html_auth: str) -> dict:
        return {
            'requestId': request['requestId'],
            'payload': self.process_fulfillment_payload(request, html_auth)
        }

    def process_fulfillment_payload(self, request: dict, html_auth: str) -> dict:
        auth_parts = html_auth.partition(' ')

        if auth_parts[0] != 'Bearer':
            return {'errorCode': 'authFailure'}

        access_token = AccessToken.objects.filter(token=auth_parts[2])

        if not access_token.exists():
            return {'errorCode': 'authFailure'}

        if timezone.now() >= access_token[0].expiration:
            return {'errorCode': 'authExpired'}

        inputs = request['inputs']

        if len(inputs) > 1:
            print('/!\\ Multiple intents received!: %s' % str(inputs))

        current_input = inputs[0]
        response = self._fulfillment_methods[current_input['intent']](request)

        return response

    @staticmethod
    def process_sync(request: dict) -> dict:
        return {
            'agentUserId': '1836.15267389',
            'devices': [
                device.get_description() for device in Device.objects.all()
            ]
        }

    @staticmethod
    def process_query(request: dict) -> dict:
        return {
            'devices': {
                device.id: device.get_query_status() for device in Device.objects.all()
            }
        }

    @staticmethod
    def process_execute(request: dict) -> dict:
        result_commands = []

        for command in request['inputs'][0]['payload']['commands']:
            device_ids = [device['id'] for device in command['devices']]

            devices = Device.objects.filter(id__in=device_ids)

            for device in devices:
                for e in command['execution']:
                    # warning: if grouped commands are sent, this will output them separately
                    result_commands.append(device.execute_command(e['command'], e['params']))

        return {
            'commands': result_commands
        }

    @staticmethod
    def process_disconnect(request: dict) -> dict:
        return {}
