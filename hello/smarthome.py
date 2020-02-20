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
    return methods[current_input['intent']](current_input)


def process_sync(request: dict) -> dict:
    return {
        'requestId': request['requestId'],
        'payload': {
            'agentUserId': '1836.15267389',
            'devices': [device_sync(device) for device in Device.objects.all()]
        }
    }


def process_query(request: dict) -> dict:
    devices = {}

    for device in Device.objects.all():
        devices[device.id] = device_query_status(device)

    return {
        'requestId': request['requestId'],
        'payload': {
            'devices': devices
        }
    }


def process_execute(request: dict) -> dict:
    raise NotImplementedError


def process_disconnect(request: dict) -> dict:
    return {}


def device_sync(device: Device) -> dict:
    return {
        'id': device.id,
        'name': {'name': device.name},
        'type': device.type,
        'traits': [trait for trait in device.traits],
        'attributes': device.attributes,
        'willReportState': device.will_report_state
    }


def device_query_status(device):
    device_status = {'online': True, 'status': 'SUCCESS'}

    for trait in device.traits:
        name, status = __trait_status_methods[trait]()
        device_status[name] = status

    return device_status


__trait_status_methods = {
    Device.Trait.ON_OFF: lambda: ('on', True)
}
