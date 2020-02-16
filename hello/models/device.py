from django.db.models import Model, ManyToManyField, TextChoices, CharField


class DeviceType(TextChoices):
    LIGHT = 'action.devices.types.LIGHT'


class DeviceTrait(TextChoices):
    ON_OFF = 'action.devices.traits.OnOff'


class DeviceTraitEntry(Model):
    trait = CharField(primary_key=True, max_length=64, choices=DeviceTrait.choices)


class Device(Model):
    id = CharField(primary_key=True, max_length=32)
    type = CharField(max_length=64, choices=DeviceType.choices)
    traits = ManyToManyField(DeviceTraitEntry)
    # name
    # willReportState
    # attributes
    # deviceInfo

    def get_traits_dict(self):
        return [trait.trait for trait in self.traits.all()]

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'traits': self.get_traits_dict()
        }
