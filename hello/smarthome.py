from .models.device import Device


def process_fulfillment(request_json: dict) -> dict:
    inputs = request_json['inputs']

    if len(inputs) > 1:
        print('/!\\ Multiple intents received!: %s' % str(inputs))

    methods = {
        'action.devices.SYNC': process_sync,
        'action.devices.QUERY': process_query,
        'action.devices.EXECUTE': process_execute,
        'action.devices.DISCONNECT': process_disconnect,
    }

    current_input = inputs[0]
    return methods[current_input['intent']](request_json)


def process_sync(request: dict) -> dict:
    return {
        'requestId': request['requestId'],
        'payload': {
            'agentUserId': '1836.15267389',
            'devices': [
                device.get_description() for device in Device.get_all_devices()
            ]
        }
    }


def process_query(request: dict) -> dict:
    return {
        'requestId': request['requestId'],
        'payload': {
            'devices': {
                device.id: device.get_query_status() for device in Device.get_all_devices()
            }
        }
    }


def process_execute(request: dict) -> dict:
    result_commands = []

    for command in request['inputs'][0]['payload']['commands']:
        device_ids = [device['id'] for device in command['devices']]

        devices = Device.get_devices(device_ids)

        for device in devices:
            for e in command['execution']:
                # això no acaba d'estar bé perquè si s'agrupen comandes en enviar, aquí queden separades
                result_commands.append(device.execute(e['command'], e['params']))

    return {
        'requestId': request['requestId'],
        'payload': {
            'commands': result_commands
        }
    }


def process_disconnect(request: dict) -> dict:
    return {}
