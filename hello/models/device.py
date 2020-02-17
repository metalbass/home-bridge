from django.db.models import Model, OneToOneField, ManyToManyField, PROTECT, TextChoices, CharField, BooleanField
from collectionfield.models import CollectionField


class DeviceType(TextChoices):
    LIGHT = 'action.devices.types.LIGHT'


class DeviceTrait(TextChoices):
    ON_OFF = 'action.devices.traits.OnOff'


class DeviceName(Model):
    default_names = CollectionField(collection_type=set, item_type=str, unique=True)
    name = CharField(max_length=64)
    nick_names = CollectionField(collection_type=set, item_type=str, unique=True)

    def get_name_dict(self):
        return {
            'defaultNames': [name for name in self.default_names],
            'name': self.name,
            'nicknames': [name for name in self.nick_names]
        }


class Device(Model):
    id = CharField(primary_key=True, max_length=32)
    type = CharField(max_length=64, choices=DeviceType.choices)
    traits = CollectionField(collection_type=set, item_type=DeviceTrait, choices=DeviceTrait.choices)
    name = OneToOneField(DeviceName, on_delete=PROTECT, null=True)
    will_report_state = BooleanField(default=False)
    # attributes
    # deviceInfo

    def get_traits_dict(self):
        return [trait for trait in self.traits]

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'traits': self.get_traits_dict(),
            'name': self.name.get_name_dict(),
            'willReportState': self.will_report_state
        }
