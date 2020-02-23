from abc import abstractmethod

from django.db.models import Model, TextChoices, CharField, BooleanField, IntegerField


class Device(Model):
    class AbstractModelObjects:
        def all(self):
            result = []

            for cls in self._get_subclasses():
                result.extend(list(cls.objects.all()))

            return result

        def filter(self, **kwargs):
            result = []

            for cls in self._get_subclasses():
                result.extend(list(cls.objects.filter(**kwargs)))

            return result

        def _get_subclasses(self) -> list:
            return [
                Blind,
                Bed
            ]


    objects = AbstractModelObjects()

    class Type:
        LIGHT = 'action.devices.types.LIGHT'
        BLINDS = 'action.devices.types.BLINDS'
        BED = 'action.devices.types.BED'

    class Trait:
        ON_OFF = 'action.devices.traits.OnOff'
        OPEN_CLOSE = 'action.devices.traits.OpenClose'

    class Command:
        OPEN_CLOSE = 'action.devices.commands.OpenClose'

    class Meta:
        abstract = True

    id = CharField(primary_key=True, max_length=32)
    name = CharField(max_length=64, unique=True)
    will_report_state = BooleanField(default=False)

    @abstractmethod
    def get_type(self) -> str:
        pass

    @abstractmethod
    def get_traits(self) -> list:
        pass

    @abstractmethod
    def get_attributes(self) -> dict:
        pass

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
        pass

    @abstractmethod
    def execute_command(self, command: str, params):
        pass


class Blind(Device):
    class Direction(TextChoices):
        UP = 'UP',
        DOWN = 'DOWN'

    open_percent = IntegerField(default=0)

    def get_type(self) -> str:
        return Device.Type.BLINDS

    def get_traits(self) -> list:
        return [
            Device.Trait.OPEN_CLOSE
        ]

    def get_attributes(self) -> dict:
        return {'openDirection': ['UP', 'DOWN']}

    def get_query_status(self) -> dict:
        return {
            'online': True,
            'openPercent': self.open_percent,
        }

    def execute_command(self, command: str, params):
        print('Blinds running %s: %s' % (command, params))

        print('Open percent: %s' % self.open_percent)

        if command == Device.Command.OPEN_CLOSE:
            self.open_percent = 100 - self.open_percent
            self.save()

            print('Open percent: %s' % self.open_percent)

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
