from abc import abstractmethod

from django.db.models import Model, CharField, BooleanField, IntegerField

from .managers import AbstractManager


class Device(Model):
    objects = AbstractManager()

    class Type:
        LIGHT = 'action.devices.types.LIGHT'
        BLINDS = 'action.devices.types.BLINDS'
        BED = 'action.devices.types.BED'

    class Trait:
        ON_OFF = 'action.devices.traits.OnOff'
        OPEN_CLOSE = 'action.devices.traits.OpenClose'

    class Command:
        ON_OFF = 'action.devices.commands.OnOff'
        OPEN_CLOSE = 'action.devices.commands.OpenClose'

    class Meta:
        abstract = True

    id = CharField(primary_key=True, max_length=32)
    name = CharField(max_length=64, unique=True)
    will_report_state = BooleanField(default=False)

    @abstractmethod
    def get_type(self) -> str:
        """ returns the type of this device as a string """

    @abstractmethod
    def get_traits(self) -> list:
        """ returns the supported traits for this device """

    @abstractmethod
    def get_attributes(self) -> dict:
        """ returns the attributes associated with the traits of this device """

    def get_description(self) -> dict:
        return {
            'id': self.id,
            'name': {'name': self.name},
            'type': self.get_type(),
            'traits': [trait for trait in self.get_traits()],
            'attributes': self.get_attributes(),
            'willReportState': self.will_report_state
        }

    @abstractmethod
    def get_query_status(self) -> dict:
        """ returns the status of the device in the query intent format """

    @abstractmethod
    def execute_command(self, command: str, params: dict) -> dict:
        """ returns the status of the device in the execute intent format """


Device.objects = AbstractManager(Device)


class Blind(Device):
    open_percent = IntegerField(default=0)

    def get_type(self) -> str:
        return Device.Type.BLINDS

    def get_traits(self) -> list:
        return [
            Device.Trait.OPEN_CLOSE
        ]

    def get_attributes(self) -> dict:
        return {
            'openDirection': ['UP', 'DOWN']
        }

    def get_query_status(self) -> dict:
        return {

            'online': True,
            'openPercent': self.open_percent,
        }

    def execute_command(self, command: str, params: dict) -> dict:
        if command == Device.Command.OPEN_CLOSE:
            self.open_percent = params['openPercent']
            self.save()

            return {
                'ids': [self.id],
                'states': {'online': True, 'openPercent': self.open_percent},
                'status': 'SUCCESS'
            }


class Bed(Device):
    def get_type(self) -> str:
        return Device.Type.BED

    def get_traits(self) -> list:
        return []

    def get_attributes(self) -> dict:
        return {}

    def get_query_status(self) -> dict:
        return {}

    def execute_command(self, command: str, params: dict) -> dict:
        pass
