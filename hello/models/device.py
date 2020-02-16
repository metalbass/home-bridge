from django.db.models import Model, OneToOneField, ManyToManyField, PROTECT, TextChoices, CharField, BooleanField
# from collectionfield.models import CollectionField


class DeviceType(TextChoices):
    LIGHT = 'action.devices.types.LIGHT'


class DeviceTrait(TextChoices):
    ON_OFF = 'action.devices.traits.OnOff'


class DeviceTraitEntry(Model):
    trait = CharField(primary_key=True, max_length=64, choices=DeviceTrait.choices)


class DeviceName(Model):
    # default_names = CollectionField(collection_type=set, item_type=str, unique=True)
    name = CharField(max_length=64)
    # nick_names = CollectionField(collection_type=set, item_type=str, unique=True)


class Device(Model):
    id = CharField(primary_key=True, max_length=32)
    type = CharField(max_length=64, choices=DeviceType.choices)
    traits = ManyToManyField(DeviceTraitEntry)
    name = OneToOneField(DeviceName, on_delete=PROTECT, null=True)
    willReportState = BooleanField(default=False)
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
