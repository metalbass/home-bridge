from collectionfield.models import CollectionField
from django.db.models import Model, TextChoices, CharField, BooleanField


class Device(Model):
    class Type(TextChoices):
        LIGHT = 'action.devices.types.LIGHT'
        BLINDS = 'action.devices.types.BLINDS'

    class Trait(TextChoices):
        ON_OFF = 'action.devices.traits.OnOff'
        OPEN_CLOSE = 'action.devices.traits.OpenClose'

    id = CharField(primary_key=True, max_length=32)
    name = CharField(max_length=64, unique=True)
    type = CharField(max_length=64, choices=Type.choices)
    traits = CollectionField(collection_type=set, item_type=Trait, choices=Trait.choices)
    attributes = CharField(max_length=1024, default='{}')
    will_report_state = BooleanField(default=False)
