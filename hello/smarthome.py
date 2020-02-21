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
    raise NotImplementedError


def process_disconnect(request: dict) -> dict:
    return {}
