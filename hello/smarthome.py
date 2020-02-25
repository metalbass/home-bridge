from .models.devices import Device


class SmartHome:
    def __init__(self):
        self._fulfillment_methods = {
            'action.devices.SYNC': self.process_sync,
            'action.devices.QUERY': self.process_query,
            'action.devices.EXECUTE': self.process_execute,
            'action.devices.DISCONNECT': self.process_disconnect,
        }

    def process_fulfillment(self, request_json: dict) -> dict:
        inputs = request_json['inputs']

        if len(inputs) > 1:
            print('/!\\ Multiple intents received!: %s' % str(inputs))

        current_input = inputs[0]
        return self._fulfillment_methods[current_input['intent']](request_json)

    @staticmethod
    def process_sync(request: dict) -> dict:
        return {
            'requestId': request['requestId'],
            'payload': {
                'agentUserId': '1836.15267389',
                'devices': [
                    device.get_description() for device in Device.objects.all()
                ]
            }
        }

    @staticmethod
    def process_query(request: dict) -> dict:
        return {
            'requestId': request['requestId'],
            'payload': {
                'devices': {
                    device.id: device.get_query_status() for device in Device.objects.all()
                }
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
                    # això no acaba d'estar bé perquè si s'agrupen comandes en enviar, aquí queden separades
                    result_commands.append(device.execute_command(e['command'], e['params']))

        return {
            'requestId': request['requestId'],
            'payload': {
                'commands': result_commands
            }
        }

    @staticmethod
    def process_disconnect(request: dict) -> dict:
        return {}
