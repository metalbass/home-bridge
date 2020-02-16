import array


def on_sync_devices() -> array:
    device = {
        'id': '456',
        'type': 'action.devices.types.LIGHT',
        'traits': [
            'action.devices.traits.OnOff',
            'action.devices.traits.Brightness',
            'action.devices.traits.ColorTemperature',
            'action.devices.traits.ColorSpectrum'
        ],
        'name': {
            'defaultNames': [
                'lights out inc. bulb A19 color hyperglow'
            ],
            'name': 'lamp1',
            'nicknames': [
                'reading lamp'
            ]
        },
        'willReportState': False,
        'attributes': {
            'temperatureMinK': 2000,
            'temperatureMaxK': 6500
        },
        'deviceInfo': {
            'manufacturer': 'lights out inc.',
            'model': 'hg11',
            'hwVersion': '1.2',
            'swVersion': '5.4'
        }
    }

    return [
        device
    ]


def on_sync(request: dict) -> dict:
    result = {
        'requestId': request['requestId'],
        'payload': {
            'agentUserId': '1836.15267389',
            'devices': on_sync_devices()
        }
    }

    return result
