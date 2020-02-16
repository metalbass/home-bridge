from enum import Enum
from django.db.models import Model, CharField


class DeviceTypes(Enum):
    LIGHT = "action.devices.types.LIGHT"

    @classmethod
    def as_choice_list(cls):
        return [(value, value.value) for value in DeviceTypes]


class Device(Model):
    id = CharField(primary_key=True, max_length=32)
    type = CharField(max_length=64, choices=DeviceTypes.as_choice_list(), default=DeviceTypes.LIGHT)
    # traits: [ 'action.devices.traits.OnOff', 'action.devices.traits.Brightness' ],
    # name
    # willReportState
    # roomHint
    # attributes
    # deviceInfo
    # customData
