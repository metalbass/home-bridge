from collectionfield.models import CollectionField
from django.db.models import Model, TextChoices, CharField, BooleanField


class Device(Model):
    class Type(TextChoices):
        LIGHT = 'action.devices.types.LIGHT'

    class Trait(TextChoices):
        ON_OFF = 'action.devices.traits.OnOff'

    id = CharField(primary_key=True, max_length=32)
    name = CharField(max_length=64, unique=True)
    type = CharField(max_length=64, choices=Type.choices)
    traits = CollectionField(collection_type=set, item_type=Trait, choices=Trait.choices)
    will_report_state = BooleanField(default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': {'name': self.name},
            'type': self.type,
            'traits': [trait for trait in self.traits],
            'willReportState': self.will_report_state
        }
