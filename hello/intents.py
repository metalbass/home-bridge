import array
from .models.device import Device


def on_sync_devices() -> array:
    all_devices = Device.objects.all()

    return [device.to_dict() for device in all_devices]


def on_sync(request: dict) -> dict:
    result = {
        'requestId': request['requestId'],
        'payload': {
            'agentUserId': '1836.15267389',
            'devices': on_sync_devices()
        }
    }

    return result
